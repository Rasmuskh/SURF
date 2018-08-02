//=============================================================================
// HardwareInterface.cpp
//=============================================================================
// abstraction.......Implementation of the GPIB interface to access to
//                   the CornerStone 130 monochromator     
// class.............HardwareInterface 
// original author...J. GOUNO - NEXEYA-FRANCE
//=============================================================================

//=============================================================================
// DEPENDENCIES
//=============================================================================
#include "HardwareInterface.h"
#include <yat/utils/String.h>
#include <yat/utils/StringTokenizer.h>

namespace CornerStone130_ns
{

//=============================================================================
//- Check GPIB proxy
//=============================================================================
#define CHECK_GPIB_PROXY \
if (!m_gpibProxy) \
{ \
	THROW_DEVFAILED(_CPTC("INTERNAL_ERROR"), \
				    _CPTC("Request aborted - the GPIB proxy isn't properly initialized "), \
					_CPTC("HardwareInterface::check_gpib_proxy")); \
}

//=============================================================================
// HardwareInterface::HardwareInterface
//=============================================================================
HardwareInterface::HardwareInterface (Tango::DeviceImpl * host_device, 
                                      std::string gpib_device,
                                      double polling_period,
                                      double read_delay,
                                      double grating_write_delay, 
                                      double filter_write_delay, 
                                      double wl_write_delay)
: yat4tango::DeviceTask(host_device)
{
  m_gpibDevice = gpib_device;
  m_filter_number = 1;
  m_filter_label = "";
  m_grating_number = 1;
  m_grating_label = "";
  m_shutter_st = E_NONE;
  m_gpibProxy = NULL;
  m_state = Tango::INIT;
  m_status = "Init in progress...";
  m_init_ok = false;
  m_timer_started = false;

  m_polling_period = polling_period;
  m_read_delay = read_delay;
  m_grating_delay = grating_write_delay;
  m_filter_delay = filter_write_delay;
  m_wl_delay = wl_write_delay;
  m_current_delay = 0.0;
  m_wl_range = 0.0;

	this->set_timeout_msg_period (0xFFFF);
	this->enable_timeout_msg (false);

	this->set_periodic_msg_period (0xFFFF);
	this->enable_periodic_msg (false);
}

//=============================================================================
// HardwareInterface::~HardwareInterface()
//=============================================================================
HardwareInterface::~HardwareInterface()
{
  this->enable_periodic_msg(false);

  if (m_gpibProxy)
  {
    delete (m_gpibProxy);
    m_gpibProxy = NULL;
  }
}

//=============================================================================
// HardwareInterface::open_com()
//=============================================================================
void HardwareInterface::open_com()
  throw (Tango::DevFailed)
{
  m_init_ok = false;
  m_state = Tango::INIT;
  m_status = "Init in progress...";

  // open GPIB device proxy
	try
	{
		m_gpibProxy = new Tango::DeviceProxy(m_gpibDevice);
    
    if (m_gpibProxy)
    {
      // ping GPIB device
	    int l_res = m_gpibProxy->ping();
	    DEBUG_STREAM << "The GPIB Device proxy pings at " << l_res << std::endl;
    }
  }
	catch (...)
	{
    m_state = Tango::FAULT;
    m_status = "GPIB device error";
		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
			_CPTC("Cannot create proxy on GPIB Device. Check device name or state!"),
			_CPTC("HardwareInterface::open_com"));
	}

	CHECK_GPIB_PROXY;

	Tango::DeviceData l_data;
	Tango::DeviceData l_data_ret;
  std::string l_info_str;

	try
	{
		//- send INFO request to monochromator
		Tango::DevString l_str = kGET_INFO;
		l_data << l_str;
		l_data_ret = m_gpibProxy->command_inout("WriteRead", l_data);
    l_data_ret >> l_info_str;
    DEBUG_STREAM << "INFO request: " << l_info_str << std::endl;
	}
	catch (Tango::DevFailed &e)
	{
    m_state = Tango::FAULT;
    m_status = "GPIB device error";

		ERROR_STREAM << e << std::endl;
		RETHROW_DEVFAILED(e, 
      _CPTC("DEVICE_ERROR"), 
			_CPTC("Cannot get monochromator INFO: hardware error!"), 
			_CPTC("HardwareInterface::open_com")); 
	}
	catch (...)
	{
    m_state = Tango::FAULT;
    m_status = "GPIB device error";

    ERROR_STREAM << "INFO request error!" << std::endl;
		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
      _CPTC("Cannot get monochromator INFO: hardware error!"),
			_CPTC("HardwareInterface::open_com"));
	}
	
  // check hardware error
  std::string l_err_msg;
  if (check_error(l_err_msg))
  {
    m_state = Tango::FAULT;
    m_status = std::string("Error on INFO request: ") + l_err_msg;

		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
      _CPTC("Cannot get monochromator INFO: hardware error!"),
			_CPTC("HardwareInterface::open_com"));
	}

  // wait a little to let hardware execute the previous command
  usleep(m_read_delay * 1000); // in 탎

  m_state = Tango::STANDBY;
  m_status = "Device is up and ready";
  m_init_ok = true;
}

// ============================================================================
// HardwareInterface::process_message
// ============================================================================
void HardwareInterface::process_message (yat::Message& msg)
  throw (Tango::DevFailed)
{

	//- handle msg
	switch (msg.type())
	{
		//- THREAD_INIT ----------------------
	case yat::TASK_INIT:
		{
			DEBUG_STREAM << "HardwareInterface::handle_message::THREAD_INIT::thread is starting up" << std::endl;
	    // start periodic msg
      this->set_periodic_msg_period((size_t)this->m_polling_period); //ms
	    this->enable_periodic_msg(true);
		} 
		break;

		//- THREAD_EXIT ----------------------
	case yat::TASK_EXIT:
		{
			DEBUG_STREAM << "HardwareInterface::handle_message::THREAD_EXIT::thread is quitting" << std::endl;
		}
		break;

		//- THREAD_PERIODIC ------------------
	case yat::TASK_PERIODIC:
		{
			DEBUG_STREAM << "HardwareInterface::handle_message::THREAD_PERIODIC" << std::endl;
			this->periodic_job_i();
		}
		break;

		//- THREAD_TIMEOUT -------------------
	case yat::TASK_TIMEOUT:
		{
      //- noop
		}
		break;

		//- kSET_WAVE_LENGTH_MSG
	case kSET_WAVE_LENGTH_MSG:
		{
      DEBUG_STREAM << "HardwareInterface::handle_message::kSET_WAVE_LENGTH_MSG" << std::endl;
      double wl = msg.get_data<double>();
			this->set_wavelength_i(wl);
		}
		break;

		//- kSET_FILTER_MSG
	case kSET_FILTER_MSG:
		{
      DEBUG_STREAM << "HardwareInterface::handle_message::kSET_FILTER_MSG" << std::endl;
      yat::uint16 nb = msg.get_data<yat::uint16>();
		  this->set_filter_nb_i(nb);
		}
		break;

		//- kSET_GRATING_MSG
	case kSET_GRATING_MSG:
		{
      DEBUG_STREAM << "HardwareInterface::handle_message::kSET_GRATING_MSG" << std::endl;
      yat::uint16 nb = msg.get_data<yat::uint16>();
      this->set_grating_nb_i(nb);
		}
		break;

		//- kSHUTTER_STATE_MSG
	case kSHUTTER_STATE_MSG:
		{
      DEBUG_STREAM << "HardwareInterface::handle_message::kSHUTTER_STATE_MSG" << std::endl;
      E_shutter_state_t st = msg.get_data<E_shutter_state_t>();
		  this->set_shutter_state_i(st);
		}
		break;

		//- kABORT_MSG
	case kABORT_MSG:
		{
      DEBUG_STREAM << "HardwareInterface::handle_message::kABORT_MSG" << std::endl;
      this->abort_i();
		}
		break;

  //- UNHANDLED MSG --------------------
	default:
		DEBUG_STREAM << "HardwareInterface::handle_message::unhanded msg type received" << std::endl;
		break;
	}
}

//=============================================================================
// HardwareInterface::get_state_and_status()
//=============================================================================
Tango::DevState HardwareInterface::get_state_and_status(std::string& status)
{
  // updated by periodic job
  yat::AutoMutex<> guard(this->m_dataLock);
  status = m_status;
  return m_state;
}

//=============================================================================
// HardwareInterface::update_state_and_status()
//=============================================================================
void HardwareInterface::update_state_and_status()
{
  DEBUG_STREAM << "HardwareInterface::update_state_and_status() entering..." << std::endl;

  if (!m_init_ok)
  {
    // should not be here, but in case...
    m_state = Tango::INIT;
    m_status = "Init in progress...";
    return;
  }

  if (!m_gpibProxy)
  {
    m_state = Tango::FAULT;
    m_status = "GPIB proxy not defined!";
    return;
  }

	//- get GPIB device state
	Tango::DevState l_gpib_state = m_gpibProxy->state();
  m_status = std::string("GPIB Device state: ") + std::string(Tango::DevStateName[l_gpib_state]) + std::string("\n");

  // check hardware error
  std::string l_err_msg;
  if (check_error(l_err_msg))
  {
		m_state = Tango::FAULT;
    m_status += std::string("Monochromator error: ") + l_err_msg;
	}
  else
  {
	  m_status += std::string("Device is up and ready");	
    m_state = Tango::STANDBY;
  }
}

//=============================================================================
// HardwareInterface::get_grating_label()
//=============================================================================
std::string HardwareInterface::get_grating_label() 
{
  // updated by periodic job
  yat::AutoMutex<> guard(this->m_dataLock);
  return m_grating_label;
}

//=============================================================================
// HardwareInterface::update_grating_label()
//=============================================================================
void HardwareInterface::update_grating_label()
  throw (Tango::DevFailed)
{
  DEBUG_STREAM << "HardwareInterface::update_grating_label() entering..." << std::endl;

	CHECK_GPIB_PROXY;
	
	Tango::DeviceData l_data;
	Tango::DevString  l_request;
	Tango::DeviceData l_data_ret;
	std::string l_requestLabel;	

	//- get current grating label according to current grating number
	char l_buff[50];
	memset(l_buff, 0, 50);
	sprintf(l_buff, kGET_GRATING_LABEL, m_grating_number);
	l_request = Tango::string_dup(l_buff);
	l_data << l_request;
  DEBUG_STREAM << "Send grating label request on monochromator: " << l_buff << std::endl;
	
	try
	{
		l_data_ret = m_gpibProxy->command_inout("WriteRead", l_data);
	  l_data_ret >> l_requestLabel;
    DEBUG_STREAM << "Request answer: " << l_requestLabel << std::endl;
	}
	catch (Tango::DevFailed &e)
	{
		ERROR_STREAM << e << std::endl;
		RETHROW_DEVFAILED(e, 
      _CPTC("DEVICE_ERROR"), 
			_CPTC("Cannot get monochromator grating label: hardware error!"), 
			_CPTC("HardwareInterface::update_grating_label")); 
	}
	catch (...)
	{
		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
			_CPTC("Cannot get monochromator grating label: hardware error!"),
			_CPTC("HardwareInterface::update_grating_label"));
	}	

	yat::String l_str_to_trim;
	l_str_to_trim = l_requestLabel.data();
	l_str_to_trim.trim();
	
  m_grating_label = (std::string)l_str_to_trim;
}

//=============================================================================
// HardwareInterface::set_grating_range()
//=============================================================================
void HardwareInterface::set_grating_range(double wl_range)
{
  yat::AutoMutex<> guard(this->m_dataLock);
  m_wl_range = wl_range;
}

//=============================================================================
// HardwareInterface::set_grating_label()
//=============================================================================
void HardwareInterface::set_grating_label(yat::uint16 gratNb, std::string gratLabel)
  throw (Tango::DevFailed)
{
	CHECK_GPIB_PROXY;

	Tango::DeviceData l_data;
	Tango::DevString  l_request;
	Tango::DeviceData l_data_ret;
	
	char l_buff[50];
	memset(l_buff, 0, 50);
	sprintf(l_buff, kSET_GRATING_LABEL, gratNb, gratLabel.c_str());
	l_request = Tango::string_dup(l_buff);
	l_data << l_request;
  DEBUG_STREAM << "Send grating label command on monochromator: " << l_buff << std::endl;
	
	try
	{
		m_gpibProxy->command_inout("Write", l_data );
	}
	catch (Tango::DevFailed &e)
	{
		ERROR_STREAM << e << std::endl;
		RETHROW_DEVFAILED(e, 
      _CPTC("DEVICE_ERROR"), 
			_CPTC("Cannot set monochromator grating label: hardware error!"), 
			_CPTC("HardwareInterface::set_grating_label")); 
	}
	catch (...)
	{
		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
			_CPTC("Cannot set monochromator grating label: hardware error!"),
			_CPTC("HardwareInterface::set_grating_label"));
	}	
	
  // check hardware error
  std::string l_err_msg;
  if (check_error(l_err_msg))
  {
		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
			l_err_msg.c_str(),
			_CPTC("HardwareInterface::set_grating_label"));
	}

  // wait a little to let hardware execute the previous command
  usleep(m_read_delay * 1000); // in 탎
}

//=============================================================================
// HardwareInterface::get_grating_nb()
//=============================================================================
yat::uint16 HardwareInterface::get_grating_nb() 
{
  // updated by periodic job
  yat::AutoMutex<> guard(this->m_dataLock);
  return m_grating_number;
}

//=============================================================================
// HardwareInterface::update_grating_nb()
//=============================================================================
void HardwareInterface::update_grating_nb() 
  throw (Tango::DevFailed)
{
  DEBUG_STREAM << "HardwareInterface::update_grating_nb() entering..." << std::endl;

	CHECK_GPIB_PROXY;
	
	yat::uint16 l_number = 0;
	Tango::DeviceData l_data;
	Tango::DeviceData l_data_ret;
	std::string l_ret_str;

	//- get grating number
  Tango::DevString l_str = kGET_GRATING_NUMBER;
  l_data << l_str;
  DEBUG_STREAM << "Send grating nb request on monochromator: " << kGET_GRATING_NUMBER << std::endl;

	try
	{		
		l_data_ret = m_gpibProxy->command_inout("WriteRead", l_data );
	  l_data_ret >> l_ret_str;
    DEBUG_STREAM << "Request answer: " << l_ret_str << std::endl;
	}
	catch (Tango::DevFailed &e)
	{
		ERROR_STREAM << e << std::endl;
		RETHROW_DEVFAILED(e, 
      _CPTC("DEVICE_ERROR"), 
			_CPTC("Cannot get monochromator grating number: hardware error!"), 
			_CPTC("HardwareInterface::update_grating_nb")); 
	}
	catch (...)
	{
		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
			_CPTC("Cannot get monochromator grating number: hardware error!"),
			_CPTC("HardwareInterface::update_grating_nb"));
	}	
	
  // extract 1st number (comma separated)
	yat::StringTokenizer tok (l_ret_str, ",");
	l_number = tok.next_int_token();

	m_grating_number = l_number;
}	

//=============================================================================
// HardwareInterface::set_grating_nb()
//=============================================================================
void HardwareInterface::set_grating_nb(yat::uint16 gratNb) 
  throw (Tango::DevFailed)
{
  yat::Message * msg = yat::Message::allocate(kSET_GRATING_MSG, MAX_USER_PRIORITY, true);
  msg->attach_data(gratNb);
  this->wait_msg_handled(msg, kDEFAULT_CMD_TMO);
}

//=============================================================================
// HardwareInterface::set_grating_nb_i()
//=============================================================================
void HardwareInterface::set_grating_nb_i(yat::uint16 gratNb) 
  throw (Tango::DevFailed)
{
	CHECK_GPIB_PROXY;
	
	yat::uint16 l_number = 0;
	Tango::DeviceData l_data;
	Tango::DevString  l_request;
	Tango::DeviceData l_data_ret;
	
	//- get grating number
	char l_buff[50];
	memset(l_buff, 0, 50);
	sprintf(l_buff, kSET_GRATING_NUMBER, gratNb);
	l_request = Tango::string_dup(l_buff);
	l_data << l_request;
  DEBUG_STREAM << "Send grating nb command on monochromator: " << l_buff << std::endl;
	
	try
	{		
		m_gpibProxy->command_inout("Write", l_data );
	}
	catch (Tango::DevFailed &e)
	{
		ERROR_STREAM << e << std::endl;
		RETHROW_DEVFAILED(e, 
      _CPTC("DEVICE_ERROR"), 
			_CPTC("Cannot set monochromator grating number: hardware error!"), 
			_CPTC("HardwareInterface::set_grating_nb_i")); 
	}
	catch (...)
	{
		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
			_CPTC("Cannot set monochromator grating number: hardware error!"),
			_CPTC("HardwareInterface::set_grating_nb_i"));
	}	
	
  // set MOVING state
  m_state = Tango::MOVING;
  m_status = "Grating change in progress...";

  // start waiting delay
	m_write_timer.restart();
  m_timer_started = true;
  m_current_delay = m_grating_delay;
}	

//=============================================================================
// HardwareInterface::get_filter_label()
//=============================================================================
std::string HardwareInterface::get_filter_label()
{
  // updated by periodic job
  yat::AutoMutex<> guard(this->m_dataLock);
  return m_filter_label;
}

//=============================================================================
// HardwareInterface::update_filter_label()
//=============================================================================
void HardwareInterface::update_filter_label() 
  throw (Tango::DevFailed)
{	
  DEBUG_STREAM << "HardwareInterface::update_filter_label() entering..." << std::endl;

	CHECK_GPIB_PROXY;
	
	Tango::DeviceData l_data;
	Tango::DevString  l_request;
	Tango::DeviceData l_data_ret;
	std::string l_requestFilter;
	
	//- get filter number
	char l_buff[50];
	memset(l_buff, 0, 50);
	sprintf(l_buff, kGET_FILTER_LABEL, m_filter_number);
	l_request = Tango::string_dup(l_buff);
	l_data << l_request;
  DEBUG_STREAM << "Send filter label request on monochromator: " << l_buff << std::endl;
	
	try
	{		
		l_data_ret = m_gpibProxy->command_inout("WriteRead", l_data);
    l_data_ret >> l_requestFilter;
    DEBUG_STREAM << "Request answer: " << l_requestFilter << std::endl;
	}
	catch (Tango::DevFailed &e)
	{
		ERROR_STREAM << e << std::endl;
		RETHROW_DEVFAILED(e, 
      _CPTC("DEVICE_ERROR"), 
			_CPTC("Cannot get monochromator filter label: hardware error!"), 
			_CPTC("HardwareInterface::update_filter_label")); 
	}
	catch (...)
	{
		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
			_CPTC("Cannot get monochromator filter label: hardware error!"),
			_CPTC("HardwareInterface::update_filter_label"));
	}	

  // check hardware error
  std::string l_err_msg;
  if (check_error(l_err_msg))
  {
    ERROR_STREAM << "Cannot get monochromator filter label! Hardware error: "
      << l_err_msg << std::endl;
		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
			l_err_msg.c_str(),
			_CPTC("HardwareInterface::update_filter_label"));
	}

	yat::String l_str_to_trim;
	l_str_to_trim = l_requestFilter.data();
	l_str_to_trim.trim();
	
	m_filter_label = l_str_to_trim;
}

//=============================================================================
// HardwareInterface::set_filter_label()
//=============================================================================
void HardwareInterface::set_filter_label(yat::uint16 filterNb, std::string filterLabel)
  throw (Tango::DevFailed)
{
	CHECK_GPIB_PROXY;

	Tango::DeviceData l_data;
	Tango::DevString  l_request;
	Tango::DeviceData l_data_ret;
	yat::String l_str_to_trim;
	
	char l_buff[50];
	memset(l_buff, 0, 50);
	sprintf(l_buff, kSET_FILTER_LABEL, filterNb, filterLabel.c_str());
	l_request = Tango::string_dup(l_buff);
	l_data << l_request;
  DEBUG_STREAM << "Send filter label command on monochromator: " << l_buff << std::endl;
	
	try
	{
		m_gpibProxy->command_inout("Write", l_data);
	}
	catch (Tango::DevFailed &e)
	{
		ERROR_STREAM << e << std::endl;
		RETHROW_DEVFAILED(e, 
      _CPTC("DEVICE_ERROR"), 
			_CPTC("Cannot set monochromator filter label: hardware error!"), 
			_CPTC("HardwareInterface::set_filter_label")); 
	}
	catch (...)
	{
		THROW_DEVFAILED(_CPTC("DEVICE_ERROR"),
			_CPTC("Cannot set monochromator filter label: hardware error!"),
			_CPTC("HardwareInterface::set_filter_label"));
	}
		
  // check hardware error
  std::string l_err_msg;
  if (check_error(l_err_msg))
  {
		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
			l_err_msg.c_str(),
			_CPTC("HardwareInterface::set_filter_label"));
	}

  // wait a little to let hardware execute the previous command
  usleep(m_read_delay * 1000); // in 탎
}

//=============================================================================
// HardwareInterface::get_filter_nb()
//=============================================================================
yat::uint16 HardwareInterface::get_filter_nb() 
{
  // updated by periodic job
  yat::AutoMutex<> guard(this->m_dataLock);
  return m_filter_number;
}

//=============================================================================
// HardwareInterface::update_filter_nb()
//=============================================================================
void HardwareInterface::update_filter_nb() 
  throw (Tango::DevFailed)
{
  DEBUG_STREAM << "HardwareInterface::update_filter_nb() entering..." << std::endl;

	CHECK_GPIB_PROXY;
	
	yat::uint16 l_nbfilter = 0;
	Tango::DeviceData l_data;
	Tango::DeviceData l_data_ret;
	std::string l_ret_str;
	
	//- get filter number
  Tango::DevString l_str = kGET_FILTER_NUMBER;
  l_data << l_str;
  DEBUG_STREAM << "Send filter nb request on monochromator: " << kGET_FILTER_NUMBER << std::endl;
	
	try
	{		
	  l_data_ret = m_gpibProxy->command_inout("WriteRead", l_data);
    l_data_ret >> l_ret_str;
    DEBUG_STREAM << "Request answer: " << l_ret_str << std::endl;
	}
	catch (Tango::DevFailed &e)
	{
		ERROR_STREAM << e << std::endl;
		RETHROW_DEVFAILED(e, 
      _CPTC("DEVICE_ERROR"), 
			_CPTC("Cannot get monochromator filter number: hardware error!"), 
			_CPTC("HardwareInterface::update_filter_nb")); 
	}
	catch (...)
	{
		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
			_CPTC("Cannot get monochromator filter number: hardware error!"),
			_CPTC("HardwareInterface::update_filter_nb"));
	}

	yat::String l_str_to_trim;
	l_str_to_trim = l_ret_str.data();
	l_str_to_trim.trim();
	l_nbfilter = (yat::uint16) atoi(l_str_to_trim.data());
	m_filter_number = l_nbfilter;
}

//=============================================================================
// HardwareInterface::set_filter_nb()
//=============================================================================
void HardwareInterface::set_filter_nb(yat::uint16 filterNb) 
  throw (Tango::DevFailed)
{
  yat::Message * msg = yat::Message::allocate(kSET_FILTER_MSG, MAX_USER_PRIORITY, true);
  msg->attach_data(filterNb);
  this->wait_msg_handled(msg, kDEFAULT_CMD_TMO);
}

//=============================================================================
// HardwareInterface::set_filter_nb_i()
//=============================================================================
void HardwareInterface::set_filter_nb_i(yat::uint16 filterNb) 
  throw (Tango::DevFailed)
{
	CHECK_GPIB_PROXY;
	
	yat::uint16 l_number = 0;
	Tango::DeviceData l_data;
	Tango::DevString  l_request;
	Tango::DeviceData l_data_ret;
	
	//- get grating number
	char l_buff[50];
	memset(l_buff, 0, 50);
	sprintf(l_buff, kSET_FILTER_NUMBER, filterNb);
	l_request = Tango::string_dup(l_buff);
	l_data << l_request;
  DEBUG_STREAM << "Send filter nb command on monochromator: " << l_buff << std::endl;
	
	try
	{		
		m_gpibProxy->command_inout("Write", l_data);
	}
	catch (Tango::DevFailed &e)
	{
		ERROR_STREAM << e << std::endl;
		RETHROW_DEVFAILED(e, 
      _CPTC("DEVICE_ERROR"), 
			_CPTC("Cannot set monochromator filter number: hardware error!"), 
			_CPTC("HardwareInterface::set_filter_nb_i")); 
	}
	catch (...)
	{
		THROW_DEVFAILED(_CPTC("DEVICE_ERROR"),
			_CPTC("Cannot set monochromator filter number: hardware error!"),
			_CPTC("HardwareInterface::set_filter_nb_i"));
	}	
	
  // set MOVING state
  m_state = Tango::MOVING;
  m_status = "Filter change in progress...";

  // start waiting delay
	m_write_timer.restart();
  m_timer_started = true;
  m_current_delay = m_filter_delay;
}	
	
//=============================================================================
// HardwareInterface::set_unit()
//=============================================================================
void HardwareInterface::set_unit(std::string unit) 
    throw (Tango::DevFailed)
{
	CHECK_GPIB_PROXY;
	
	Tango::DeviceData l_data;
	Tango::DevString  l_request;
	Tango::DeviceData l_data_ret;
	
	//- get grating number
	char l_buff[50];
	memset(l_buff, 0, 50);
	sprintf(l_buff, kSET_UNIT, unit.c_str());
	l_request = Tango::string_dup(l_buff);
	l_data << l_request;
  DEBUG_STREAM << "Send user unit command on monochromator: " << l_buff << std::endl;
	
	try
	{		
		m_gpibProxy->command_inout("Write", l_data);
	}
	catch (Tango::DevFailed &e)
	{
		ERROR_STREAM << e << std::endl;
		RETHROW_DEVFAILED(e, 
      _CPTC("DEVICE_ERROR"), 
			_CPTC("Cannot set monochromator user unit: hardware error!"), 
			_CPTC("HardwareInterface::set_unit")); 
	}
	catch (...)
	{
		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
			_CPTC("Cannot set monochromator user unit: hardware error!"),
			_CPTC("HardwareInterface::set_unit"));
	}	
	
  // check hardware error
  std::string l_err_msg;
  if (check_error(l_err_msg))
  {
		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
			l_err_msg.c_str(),
			_CPTC("HardwareInterface::set_unit"));
	}

  // wait a little to let hardware execute the previous command
  usleep(m_read_delay * 1000); // in 탎
}

//=============================================================================
// HardwareInterface::set_wavelength()
//=============================================================================
void HardwareInterface::set_wavelength(double wave)
	throw (Tango::DevFailed)
{
  yat::Message * msg = yat::Message::allocate(kSET_WAVE_LENGTH_MSG, MAX_USER_PRIORITY, true);
  msg->attach_data(wave);
  this->wait_msg_handled(msg, kDEFAULT_CMD_TMO);
}

//=============================================================================
// HardwareInterface::set_wavelength_i()
//=============================================================================
void HardwareInterface::set_wavelength_i(double wave)
	throw (Tango::DevFailed)
{
	CHECK_GPIB_PROXY;
	
	double l_number = 0.0;
	Tango::DeviceData l_data;
	Tango::DevString  l_request;
	Tango::DeviceData l_data_ret;
	
	char l_buff[50];
	memset(l_buff, 0, 50);
	sprintf(l_buff, kSET_WAVELENGTH, wave);
	l_request = Tango::string_dup(l_buff);
	l_data << l_request;
  DEBUG_STREAM << "Send wavelength command on monochromator: " << l_buff << std::endl;
	
	try
	{		
		m_gpibProxy->command_inout("Write", l_data);
	}
	catch (Tango::DevFailed &e)
	{
		ERROR_STREAM << e << std::endl;
		RETHROW_DEVFAILED(e, 
      _CPTC("DEVICE_ERROR"), 
			_CPTC("Cannot set monochromator wavelength: hardware error!"), 
			_CPTC("HardwareInterface::set_wavelength_i")); 
	}
	catch (...)
	{
		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
			_CPTC("Cannot set monochromator wavelength: hardware error!"),
			_CPTC("HardwareInterface::set_wavelength_i"));
	}	
	
  // set MOVING state
  m_state = Tango::MOVING;
  m_status = "Wave length change in progress...";

  // start waiting delay
	m_write_timer.restart();
  m_timer_started = true;
  m_current_delay = (fabs(m_wavelength_readback - wave) * m_wl_delay) / m_wl_range;
  DEBUG_STREAM << "Set new wave length: compute proportional delay = " << m_current_delay << " in ms" << std::endl;
}

//=============================================================================
// HardwareInterface::get_wavelength()
//=============================================================================
double HardwareInterface::get_wavelength()
{
  // updated by periodic job
  yat::AutoMutex<> guard(this->m_dataLock);
  return m_wavelength_readback;
}

//=============================================================================
// HardwareInterface::update_wavelength()
//=============================================================================
void HardwareInterface::update_wavelength()
	throw (Tango::DevFailed)
{
  DEBUG_STREAM << "HardwareInterface::update_wavelength() entering..." << std::endl;

	CHECK_GPIB_PROXY;
	
	double l_wave = 0.0;
	Tango::DeviceData l_data;
	Tango::DeviceData l_data_ret;
  std::string l_ret_str;
	
	//- get current wavelength
  Tango::DevString l_str = kGET_WAVELENGTH;
  l_data << l_str;  	
  DEBUG_STREAM << "Send wavelength request on monochromator: " << kGET_WAVELENGTH << std::endl;
	
	try
	{		
		l_data_ret = m_gpibProxy->command_inout("WriteRead", l_data);
	  l_data_ret >> l_ret_str;
    DEBUG_STREAM << "Request answer: " << l_ret_str << std::endl;
	}
	catch (Tango::DevFailed &e)
	{
		ERROR_STREAM << e << std::endl;
		RETHROW_DEVFAILED(e, 
      _CPTC("DEVICE_ERROR"), 
			_CPTC("Cannot get monochromator wavelength: hardware error!"), 
			_CPTC("HardwareInterface::update_wavelength")); 
	}
	catch (...)
	{
		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
			_CPTC("Cannot get monochromator wavelength: hardware error!"),
			_CPTC("HardwareInterface::update_wavelength"));
	}
	
  yat::String l_str_to_trim;
	l_str_to_trim = l_ret_str.data();
	l_str_to_trim.trim();
	l_wave = (double) atof(l_str_to_trim.data());
		
  // store readback value
  m_wavelength_readback = l_wave;
}	

//=============================================================================
// HardwareInterface::get_shutter_state()
//=============================================================================
E_shutter_state_t HardwareInterface::get_shutter_state()
{
  // updated by periodic job
  yat::AutoMutex<> guard(this->m_dataLock);
  return m_shutter_st;
}

//=============================================================================
// HardwareInterface::update_shutter_state()
//=============================================================================
void HardwareInterface::update_shutter_state()
  throw  (Tango::DevFailed)
{
  CHECK_GPIB_PROXY;
	
  Tango::DeviceData l_data;
  Tango::DeviceData l_data_ret;
  std::string l_ret_str;
	
  //- get filter number
  Tango::DevString l_str = kGET_SHUTTER;
  l_data << l_str; 	
  DEBUG_STREAM << "Send shutter state request on monochromator: " << kGET_SHUTTER << std::endl;
	
  try
  {		
    l_data_ret = m_gpibProxy->command_inout("WriteRead", l_data);
    l_data_ret >> l_ret_str;
    DEBUG_STREAM << "Request answer: " << l_ret_str << std::endl;
  }
  catch (Tango::DevFailed &e)
  {
    ERROR_STREAM << e << std::endl;
    RETHROW_DEVFAILED(e, 
      _CPTC("DEVICE_ERROR"), 
      _CPTC("Cannot get monochromator shutter state: hardware error!"), 
      _CPTC("HardwareInterface::update_shutter_state")); 
  }
  catch (...)
  {
    THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
      _CPTC("Cannot get monochromator shutter state: hardware error!"),
      _CPTC("HardwareInterface::update_shutter_state"));
  }	
	
  yat::String l_str_to_trim;
  l_str_to_trim = l_ret_str.data();
  l_str_to_trim.trim();
  std::string l_value = l_str_to_trim.data();
 
  E_shutter_state_t l_shutter_state =  E_NONE;
  if (!l_value.compare ("C"))
  {
    l_shutter_state = E_CLOSED;
  }
  else if (!l_value.compare ("O"))
  {
    l_shutter_state = E_OPENED;
  }
  else
  {
    std::string err = std::string("Get unexpected shutter state: ") + l_value;
    THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
      _CPTC(err.c_str()),
      _CPTC("HardwareInterface::update_shutter_state"));
  }	
		
  m_shutter_st = l_shutter_state;
}

//=============================================================================
// HardwareInterface::set_shutter_state()
//=============================================================================
void HardwareInterface::set_shutter_state(E_shutter_state_t p_cmd)
	throw  (Tango::DevFailed)
{
  yat::Message * msg = yat::Message::allocate(kSHUTTER_STATE_MSG, MAX_USER_PRIORITY, true);
  msg->attach_data(p_cmd);
  this->wait_msg_handled(msg, kDEFAULT_CMD_TMO);
}

//=============================================================================
// HardwareInterface::set_shutter_state_i()
//=============================================================================
void HardwareInterface::set_shutter_state_i(E_shutter_state_t p_cmd)
	throw  (Tango::DevFailed)
{
	CHECK_GPIB_PROXY;
	
	Tango::DeviceData l_data;
	Tango::DeviceData l_data_ret;
	
	//- 
	if( p_cmd == E_OPENED)
  {
    Tango::DevString l_str = kSET_SHUTTER_OPENED;
    l_data << l_str; 
    DEBUG_STREAM << "Send shutter state command on monochromator: " << kSET_SHUTTER_OPENED << std::endl;
  }
	else	
  {
    Tango::DevString l_str = kSET_SHUTTER_CLOSED;
    l_data << l_str;
    DEBUG_STREAM << "Send shutter state command on monochromator: " << kSET_SHUTTER_CLOSED << std::endl;
  }

	try
	{		
		m_gpibProxy->command_inout("Write", l_data );
	}
	catch (Tango::DevFailed &e)
	{
		ERROR_STREAM << e << std::endl;
		RETHROW_DEVFAILED(e, 
      _CPTC("DEVICE_ERROR"), 
			_CPTC("Cannot set monochromator shutter state: hardware error!"), 
			_CPTC("HardwareInterface::set_shutter_state_i")); 
	}
	catch (...)
	{
		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
			_CPTC("Cannot set monochromator shutter state: hardware error!"),
			_CPTC("HardwareInterface::set_shutter_state_i"));
	}	
	
  // check hardware error
  std::string l_err_msg;
  if (check_error(l_err_msg))
  {
		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
			l_err_msg.c_str(),
			_CPTC("HardwareInterface::set_shutter_state_i"));
	}

  // wait a little to let hardware execute the previous command
  usleep(m_read_delay * 1000); // in 탎
}	

//=============================================================================
// HardwareInterface::abort()
//=============================================================================
void HardwareInterface::abort()
	throw (Tango::DevFailed)
{
  yat::Message * msg = yat::Message::allocate(kABORT_MSG, MAX_USER_PRIORITY, true);
  this->wait_msg_handled(msg, kDEFAULT_CMD_TMO);
}

//=============================================================================
// HardwareInterface::abort_i()
//=============================================================================
void HardwareInterface::abort_i()
	throw (Tango::DevFailed)
{
	CHECK_GPIB_PROXY;
	
	Tango::DeviceData l_data;
	Tango::DeviceData l_data_ret;
	
  Tango::DevString l_str = kABORT;
  l_data << l_str; 	
  DEBUG_STREAM << "Send abort command on monochromator: " << kABORT << std::endl;
	
	try
	{		
		m_gpibProxy->command_inout("Write", l_data );
	}
	catch (Tango::DevFailed &e)
	{
		ERROR_STREAM << e << std::endl;
		RETHROW_DEVFAILED(e, 
      _CPTC("DEVICE_ERROR"), 
			_CPTC("Cannot abort monochromator movement: hardware error!"), 
			_CPTC("HardwareInterface::abort_i")); 
	}
	catch (...)
	{
		THROW_DEVFAILED(
      _CPTC("DEVICE_ERROR"),
			_CPTC("Cannot abort monochromator movement: hardware error!"),
			_CPTC("HardwareInterface::abort_i"));
	}	
	
  // force current timer to stop (if any)
  if (m_timer_started)
    m_timer_started = false;

  // wait a little to let hardware execute the previous command
  usleep(m_read_delay * 1000); // in 탎
}

//=============================================================================
// HardwareInterface::check_error()
//=============================================================================
bool HardwareInterface::check_error(std::string& err_msg)
{
  DEBUG_STREAM << "HardwareInterface::check_error() entering..." << std::endl;

  err_msg = "";
  bool l_error = false;

	Tango::DeviceData l_data;
	Tango::DeviceData l_data_ret;
	std::string l_ret_str;
  yat::String l_str_to_trim;

  // check proxy
  if (!m_gpibProxy)
  {
    l_error = true;
    err_msg = "Device error! GPIB proxy not accessible!";
    return l_error;
  }

  // wait a little to let hardware execute the previous command
  usleep(m_read_delay * 1000); // in 탎
	
  //- read hardware state
  DEBUG_STREAM << "Send state request on monochromator: " << kGET_STB << std::endl;
  Tango::DevString l_str = kGET_STB;
  l_data << l_str;  
  
	try
	{
		l_data_ret = m_gpibProxy->command_inout("WriteRead", l_data);
    l_data_ret >> l_ret_str;
    DEBUG_STREAM << "Request answer: " << l_ret_str << std::endl;
	}
	catch (Tango::DevFailed &e)
	{
		ERROR_STREAM << e << std::endl;
    l_error = true;
    err_msg = e.errors[0].desc;
    return l_error;
	}
	catch (...)
	{
    l_error = true;
    err_msg = "Hardware error! Cannot get monochromator state, caught [...]!";
    return l_error;
	}
		
	//- get state result
	l_str_to_trim = l_ret_str.data();
	l_str_to_trim.trim();
	size_t l_stb_ret = (size_t)atoi(l_str_to_trim.data());

  // if no error, return
  if (l_stb_ret == 0)
  {
    // no error
    l_error = false;
    err_msg = "";
    return l_error;
  }

  // wait a little to let hardware execute the previous command
  usleep(m_read_delay * 1000); // in 탎
  
  //- state in error, read associated error message
  l_str = kGET_ERROR;
  l_data << l_str;
  DEBUG_STREAM << "Send error request on monochromator: " << kGET_ERROR << std::endl;
	
	try
	{
		l_data_ret = m_gpibProxy->command_inout("WriteRead", l_data);
    l_data_ret >> l_ret_str;
    DEBUG_STREAM << "Request answer: " << l_ret_str << std::endl;
	}
	catch (Tango::DevFailed &e)
	{
		ERROR_STREAM << e << std::endl;
    l_error = true;
    err_msg = e.errors[0].desc;
    return l_error;
	}
	catch (...)
	{
    l_error = true;
    err_msg = "Hardware error! Cannot get monochromator error details, caught [...]!";
    return l_error;
	}
	
	//- read error number
	l_str_to_trim = l_ret_str.data();
	l_str_to_trim.trim();
	size_t err_ret = (size_t)atoi(l_str_to_trim.data());
	
	DEBUG_STREAM << "Error number: " << err_ret << std::endl;
  if (err_ret <= kERRORS_SIZE)
  {
    err_msg = error_tab[err_ret].csErrDesc;
  }
  else
  {
    err_msg = "n/a";
  }

  l_error = true;
  return l_error;
}

//=============================================================================
// HardwareInterface::periodic_job_i()
//=============================================================================
void HardwareInterface::periodic_job_i()
{
  yat::AutoMutex<> guard(this->m_dataLock);

  // try to update monochromator values if not already in FAULT
  if (m_state == Tango::FAULT)
  {
    return;
  }

  // ... and not in MOVING state (cannot read anything in this state !)
  if (m_state == Tango::MOVING)
  {
    if (m_timer_started)
    {
      if (m_write_timer.elapsed_msec() >= m_current_delay)
      {
        // delay is over, set state to STANDBY
        m_state = Tango::STANDBY;
        m_timer_started = false;
      }
      else
      {
        // nothing to do, return...
        return;
      }
    }
    else
    {
      // aborting...
      m_state = Tango::STANDBY;
      m_status = "User abort";
      return;
    }
  }
  
  bool l_read_error = false;
  yat::uint16 previous_grat_nb = m_grating_number;
  yat::uint16 previous_filter_nb = m_filter_number;

  // update wavelength
  try
  {
    update_wavelength();
  }
  catch (Tango::DevFailed &e)
  {
    // read error
    l_read_error = true;
    m_status = "Periodic read error: ";
    m_status += std::string(e.errors[0].desc);
  }
  catch (...)
  {
    // unknown read error
    l_read_error = true;
    m_status = "Periodic unknown read error!";
  }

  // update grating nb (if no error)
  if (!l_read_error)
  {
    try
    {
      update_grating_nb();
    }
    catch (Tango::DevFailed &e)
    {
      // read error
      l_read_error = true;
      m_status = "Periodic read error: ";
      m_status += std::string(e.errors[0].desc);
    }
    catch (...)
    {
      // unknown read error
      l_read_error = true;
      m_status = "Periodic unknown read error!";
    }
  }

  // update grating label only if grating number has changed (if no error)
  if (!l_read_error)
  {
    try
    {
      if (previous_grat_nb != m_grating_number)
        update_grating_label();
    }
    catch (Tango::DevFailed &e)
    {
      // read error
      l_read_error = true;
      m_status = "Periodic read error: ";
      m_status += std::string(e.errors[0].desc);
    }
    catch (...)
    {
      // unknown read error
      l_read_error = true;
      m_status = "Periodic unknown read error!";
    }
  }

  // update filter nb (if no error)
  if (!l_read_error)
  {
    try
    {
      update_filter_nb();
    }
    catch (Tango::DevFailed &e)
    {
      // read error
      l_read_error = true;
      m_status = "Periodic read error: ";
      m_status += std::string(e.errors[0].desc);
    }
    catch (...)
    {
      // unknown read error
      l_read_error = true;
      m_status = "Periodic unknown read error!";
    }
  }

  // update grating label only if grating number has changed (if no error)
  if (!l_read_error)
  {
    try
    {
      if (previous_filter_nb != m_filter_number)
        update_filter_label();
    }
    catch (Tango::DevFailed &e)
    {
      // read error
      l_read_error = true;
      m_status = "Periodic read error: ";
      m_status += std::string(e.errors[0].desc);
    }
    catch (...)
    {
      // unknown read error
      l_read_error = true;
      m_status = "Periodic unknown read error!";
    }
  }

  // update shutter state (if no error)
  if (!l_read_error)
  {
    try
    {
      update_shutter_state();
    }
    catch (Tango::DevFailed &e)
    {
      // read error
      l_read_error = true;
      m_status = "Periodic read error: ";
      m_status += std::string(e.errors[0].desc);
    }
    catch (...)
    {
      // unknown read error
      l_read_error = true;
      m_status = "Periodic unknown read error!";
    }
  }

  // update state & status (if no error)
  if (!l_read_error)
    update_state_and_status();
  else
    m_state = Tango::FAULT;
}

}
