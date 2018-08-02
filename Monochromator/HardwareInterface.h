//=============================================================================
// HardwareInterface.h
//=============================================================================
// abstraction.......Implementation of the GPIB interface to access to
//                   the CornerStone 130 monochromator     
// class.............HardwareInterface 
// original author...J. GOUNO - NEXEYA-FRANCE
//=============================================================================
#ifndef _HARDWAREINTERFACE_H_
#define _HARDWAREINTERFACE_H_

//============================================================================
// DEPENDENCIES
//============================================================================
#include <tango.h>
#include <yat4tango/DeviceTask.h>
#include "TypesAndConsts.h"


namespace CornerStone130_ns {

// ============================================================================
// GPIB Commands
// ============================================================================
//- Attribute grating label
#define kGET_GRATING_LABEL "GRAT%1dLABEL?"
#define kSET_GRATING_LABEL "GRAT%1dLABEL %s"

//- Atribute grating number
#define kSET_GRATING_NUMBER "GRAT %1d"
#define kGET_GRATING_NUMBER "GRAT?"

//- Attribute filter label
#define kGET_FILTER_LABEL "FILTER%1dLABEL?"
#define kSET_FILTER_LABEL "FILTER%1dLABEL %s"

//- Attribute filter number
#define kGET_FILTER_NUMBER "FILTER?"
#define kSET_FILTER_NUMBER "FILTER %1d"

//- OperationalUnit command
#define kSET_UNIT "UNITS %2s"

//- handshake mode 
#define kSET_HANDSHAKE "HANDSHAKE %1d"

//- Attribute wavelength
#define kSET_WAVELENGTH "GOWAVE %3f"
#define kGET_WAVELENGTH "WAVE?"

//- Attribute shutter closed/opened
#define kSET_SHUTTER_CLOSED "SHUTTER C"
#define kSET_SHUTTER_OPENED "SHUTTER O"
#define kGET_SHUTTER "SHUTTER?"

//- Abort command
#define kABORT "ABORT"


//- Init command
//--------------------------------
//- equipment state
#define kGET_INFO "INFO?"

//- Equipment Current state 
#define kGET_STB "STB?"

//- State command
//-----------------
//- STB error number:
// 1    Command not understood 
// 2    Bad parameter used in Command 
// 3    Destination position for wavelength motion not allowed 
// 8    Could not home wavelength drive
//- INFO errors number:
// 6    Accessory not present (usually filter wheel)
// 7    Accessory already in specified pos
// 9    Label too long
#define kGET_ERROR "ERROR?"

//- CornerStone130: number/error decription 
//-------------------------------------------
//- CornerStone error struct
typedef struct cs130ErrDataType
{
  size_t csErr; // error number
  std::string csErrDesc; // error description
} cs130ErrDataType;

const size_t kERRORS_SIZE = 10;
static const cs130ErrDataType error_tab[kERRORS_SIZE] = 
{
  {0,  "System error"},
  {1,  "Command not understood"},
  {2,  "Bad parameter used in Command"},
	{3,  "Destination position for wavelength motion not allowed."},	
	{4,  "n/a"},
	{5,  "n/a"},
	{6,  "Accessory not present (usually filter wheel)"},
  {7,  "Accessory already in specified pos"},
	{8,  "Could not home wavelength drive"},
	{9,  "Label too long"}
};

// ============================================================================
// SOME USER DEFINED MESSAGES FOR THE TASK
// ============================================================================
#define kSET_WAVE_LENGTH_MSG      (yat::FIRST_USER_MSG + 1001)
#define kSET_FILTER_MSG           (yat::FIRST_USER_MSG + 1002)
#define kSET_GRATING_MSG          (yat::FIRST_USER_MSG + 1003)
#define kSHUTTER_STATE_MSG        (yat::FIRST_USER_MSG + 1004)
#define kABORT_MSG                (yat::FIRST_USER_MSG + 1005)

//-----------------------------------------------------------------------------
//- Default timeout value for task messages (in ms):
#define kDEFAULT_CMD_TMO 1000

// ============================================================================
// class: HardwareInterface
// ============================================================================
class HardwareInterface : public yat4tango::DeviceTask
{

public:

  //- Constructor
  HardwareInterface (Tango::DeviceImpl * host_device, std::string gpib_device, 
    double polling_period, double read_delay, double grating_write_delay, 
    double filter_write_delay, double wl_write_delay);

  //- Destructor
  ~HardwareInterface ();

  //- open communication
  void open_com()
    throw (Tango::DevFailed);

  //- Gets class state a status
  Tango::DevState get_state_and_status(std::string& status);

  //- Sets grating label
  void set_grating_label(yat::uint16 gratNb, std::string gratLabel) 
    throw (Tango::DevFailed);

  //- Sets filter label
  void set_filter_label(yat::uint16 filterNb, std::string filterLabel) 
    throw (Tango::DevFailed);

  //- Gets current grating label
  std::string get_grating_label();
  
  //- Gets current grating number
  yat::uint16 get_grating_nb();
	
  //- Sets new grating number
  void set_grating_nb(yat::uint16 gratNb) 
    throw (Tango::DevFailed);
	
  //- sets current wavelength range
  void set_grating_range(double wl_range);

  //- Gets current filter label
  std::string get_filter_label();
	
  //- Gets current filter number
  yat::uint16 get_filter_nb();
	
  //- Sets new filter number
  void set_filter_nb(yat::uint16 filterNb) 
    throw (Tango::DevFailed);
	
  //- Sets operational unit among NM, UM, WM
  void set_unit(std::string unit) 
    throw (Tango::DevFailed);

  //- Sets the new wavelength value
  void set_wavelength(double wl)
	  throw (Tango::DevFailed);

  //- Gets the current wavelength
  double get_wavelength();

  //- Gets the current shutter state 
  E_shutter_state_t get_shutter_state();
	
  //- Sets the shutter state 
  void set_shutter_state(E_shutter_state_t st)
	  throw (Tango::DevFailed);
	
  //- abort command
  void abort()
	  throw (Tango::DevFailed);
 
protected:
	//- process_message (implements yat4tango::DeviceTask pure virtual method)
	virtual void process_message (yat::Message& msg)
		throw (Tango::DevFailed);

private:
  //- Gpib device proxy
  Tango::DeviceProxy * m_gpibProxy;
  
  //- Gpib device name
  std::string m_gpibDevice;

  //- state and status
  Tango::DevState m_state;
  std::string m_status;

  //- com ok flag
  bool m_init_ok;
  
  //- current grating number, label & wl range
  yat::uint16 m_grating_number;
  std::string m_grating_label;
  double m_wl_range;

  //- current filter number & label
	yat::uint16 m_filter_number;
  std::string m_filter_label;

  //- current wavelength readback from hardware
  double m_wavelength_readback;

  //- current shutter state
  E_shutter_state_t m_shutter_st;

  //- polling period in ms
  double m_polling_period;

  //- delays in ms
  double m_read_delay;
  double m_grating_delay;
  double m_filter_delay;
  double m_wl_delay;
  double m_current_delay;

  // internal timer for delays
  yat::Timer m_write_timer;
  bool m_timer_started;


  //- mutex protection
  yat::Mutex m_dataLock;


  //- internal functions
  //-----------------------

  //- check cornerstone errors:
  //- if error, returns true and sets err_str with associated message
  //- else, returns false
  bool check_error(std::string& err_msg);

  //- periodic job
  void periodic_job_i();

  //- Sets new grating number
  void set_grating_nb_i(yat::uint16 gratNb) 
    throw (Tango::DevFailed);

  //- Sets new filter number
  void set_filter_nb_i(yat::uint16 filterNb) 
    throw (Tango::DevFailed);
	
  //- Sets the new wavelength value
  void set_wavelength_i(double wl)
	  throw (Tango::DevFailed);

  //- Sets the shutter state 
  void set_shutter_state_i(E_shutter_state_t st)
	  throw (Tango::DevFailed);
	
  //- abort command
  void abort_i()
	  throw (Tango::DevFailed);

  //- update functions
  void update_grating_label()
    throw (Tango::DevFailed);
  void update_grating_nb()
    throw (Tango::DevFailed);
  void update_filter_label()
    throw (Tango::DevFailed);
  void update_filter_nb()
    throw (Tango::DevFailed);
  void update_wavelength()
	  throw (Tango::DevFailed);
  void update_shutter_state()
    throw (Tango::DevFailed);
  void update_state_and_status();

};

}
#endif //_HARDWAREINTERFACE_H_
