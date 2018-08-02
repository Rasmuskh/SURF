//=============================================================================
//
// file :         CornerStone130Class.h
//
// description :  Include for the CornerStone130Class root class.
//                This class is the singleton class for
//                the CornerStone130 device class.
//                It contains all properties and methods which the 
//                CornerStone130 requires only once e.g. the commands.
//			
// project :      TANGO Device Server
//
// $Author: pascal_verdier $
//
// $Revision: 14110 $
// $Date: 2010-02-10 08:47:17 +0100 (Wed, 10 Feb 2010) $
//
// SVN only:
// $HeadURL: $
//
// CVS only:
// $Source$
// $Log$
// Revision 3.8  2009/04/07 10:53:56  pascal_verdier
// Tango-7 release.
// SVN tags added
//
// Revision 3.7  2008/04/07 12:01:57  pascal_verdier
// CVS put property modified.
//
// Revision 3.6  2007/10/23 14:04:30  pascal_verdier
// Spelling mistakes correction
//
// Revision 3.5  2007/09/14 14:36:08  pascal_verdier
// Add an ifdef WIN32 for dll generation
//
// Revision 3.4  2005/09/08 08:45:23  pascal_verdier
// For Pogo-4.4.0 and above.
//
// Revision 3.3  2005/03/02 14:06:15  pascal_verdier
// namespace is different than class name.
//
// Revision 3.2  2004/11/08 11:33:16  pascal_verdier
// if device property not found in database, it takes class property value if exists.
//
// Revision 3.1  2004/09/06 09:27:05  pascal_verdier
// Modified for Tango 5 compatibility.
//
//
// copyleft :     European Synchrotron Radiation Facility
//                BP 220, Grenoble 38043
//                FRANCE
//
//=============================================================================
//
//  		This file is generated by POGO
//	(Program Obviously used to Generate tango Object)
//
//         (c) - Software Engineering Group - ESRF
//=============================================================================

#ifndef _CORNERSTONE130CLASS_H
#define _CORNERSTONE130CLASS_H

#include <tango.h>
#include <CornerStone130.h>


namespace CornerStone130_ns
{//=====================================
//	Define classes for attributes
//=====================================
class shutterClosedAttrib: public Tango::Attr
{
public:
	shutterClosedAttrib():Attr("shutterClosed", Tango::DEV_BOOLEAN, Tango::READ_WRITE) {};
	~shutterClosedAttrib() {};
	
	virtual void read(Tango::DeviceImpl *dev,Tango::Attribute &att)
	{(static_cast<CornerStone130 *>(dev))->read_shutterClosed(att);}
	virtual void write(Tango::DeviceImpl *dev,Tango::WAttribute &att)
	{(static_cast<CornerStone130 *>(dev))->write_shutterClosed(att);}
	virtual bool is_allowed(Tango::DeviceImpl *dev,Tango::AttReqType ty)
	{return (static_cast<CornerStone130 *>(dev))->is_shutterClosed_allowed(ty);}
};

class wavelengthAttrib: public Tango::Attr
{
public:
	wavelengthAttrib():Attr("wavelength", Tango::DEV_DOUBLE, Tango::READ_WRITE) {};
	~wavelengthAttrib() {};
	
	virtual void read(Tango::DeviceImpl *dev,Tango::Attribute &att)
	{(static_cast<CornerStone130 *>(dev))->read_wavelength(att);}
	virtual void write(Tango::DeviceImpl *dev,Tango::WAttribute &att)
	{(static_cast<CornerStone130 *>(dev))->write_wavelength(att);}
	virtual bool is_allowed(Tango::DeviceImpl *dev,Tango::AttReqType ty)
	{return (static_cast<CornerStone130 *>(dev))->is_wavelength_allowed(ty);}
};

class filterLabelAttrib: public Tango::Attr
{
public:
	filterLabelAttrib():Attr("filterLabel", Tango::DEV_STRING, Tango::READ) {};
	~filterLabelAttrib() {};
	
	virtual void read(Tango::DeviceImpl *dev,Tango::Attribute &att)
	{(static_cast<CornerStone130 *>(dev))->read_filterLabel(att);}
	virtual bool is_allowed(Tango::DeviceImpl *dev,Tango::AttReqType ty)
	{return (static_cast<CornerStone130 *>(dev))->is_filterLabel_allowed(ty);}
};

class filterNumberAttrib: public Tango::Attr
{
public:
	filterNumberAttrib():Attr("filterNumber", Tango::DEV_USHORT, Tango::READ_WRITE) {};
	~filterNumberAttrib() {};
	
	virtual void read(Tango::DeviceImpl *dev,Tango::Attribute &att)
	{(static_cast<CornerStone130 *>(dev))->read_filterNumber(att);}
	virtual void write(Tango::DeviceImpl *dev,Tango::WAttribute &att)
	{(static_cast<CornerStone130 *>(dev))->write_filterNumber(att);}
	virtual bool is_allowed(Tango::DeviceImpl *dev,Tango::AttReqType ty)
	{return (static_cast<CornerStone130 *>(dev))->is_filterNumber_allowed(ty);}
};

class gratingMaxWLAttrib: public Tango::Attr
{
public:
	gratingMaxWLAttrib():Attr("gratingMaxWL", Tango::DEV_DOUBLE, Tango::READ) {};
	~gratingMaxWLAttrib() {};
	
	virtual void read(Tango::DeviceImpl *dev,Tango::Attribute &att)
	{(static_cast<CornerStone130 *>(dev))->read_gratingMaxWL(att);}
	virtual bool is_allowed(Tango::DeviceImpl *dev,Tango::AttReqType ty)
	{return (static_cast<CornerStone130 *>(dev))->is_gratingMaxWL_allowed(ty);}
};

class gratingMinWLAttrib: public Tango::Attr
{
public:
	gratingMinWLAttrib():Attr("gratingMinWL", Tango::DEV_DOUBLE, Tango::READ) {};
	~gratingMinWLAttrib() {};
	
	virtual void read(Tango::DeviceImpl *dev,Tango::Attribute &att)
	{(static_cast<CornerStone130 *>(dev))->read_gratingMinWL(att);}
	virtual bool is_allowed(Tango::DeviceImpl *dev,Tango::AttReqType ty)
	{return (static_cast<CornerStone130 *>(dev))->is_gratingMinWL_allowed(ty);}
};

class gratingLabelAttrib: public Tango::Attr
{
public:
	gratingLabelAttrib():Attr("gratingLabel", Tango::DEV_STRING, Tango::READ) {};
	~gratingLabelAttrib() {};
	
	virtual void read(Tango::DeviceImpl *dev,Tango::Attribute &att)
	{(static_cast<CornerStone130 *>(dev))->read_gratingLabel(att);}
	virtual bool is_allowed(Tango::DeviceImpl *dev,Tango::AttReqType ty)
	{return (static_cast<CornerStone130 *>(dev))->is_gratingLabel_allowed(ty);}
};

class gratingNumberAttrib: public Tango::Attr
{
public:
	gratingNumberAttrib():Attr("gratingNumber", Tango::DEV_USHORT, Tango::READ_WRITE) {};
	~gratingNumberAttrib() {};
	
	virtual void read(Tango::DeviceImpl *dev,Tango::Attribute &att)
	{(static_cast<CornerStone130 *>(dev))->read_gratingNumber(att);}
	virtual void write(Tango::DeviceImpl *dev,Tango::WAttribute &att)
	{(static_cast<CornerStone130 *>(dev))->write_gratingNumber(att);}
	virtual bool is_allowed(Tango::DeviceImpl *dev,Tango::AttReqType ty)
	{return (static_cast<CornerStone130 *>(dev))->is_gratingNumber_allowed(ty);}
};

//=========================================
//	Define classes for commands
//=========================================
class AbortClass : public Tango::Command
{
public:
	AbortClass(const char   *name,
	               Tango::CmdArgType in,
				   Tango::CmdArgType out,
				   const char        *in_desc,
				   const char        *out_desc,
				   Tango::DispLevel  level)
	:Command(name,in,out,in_desc,out_desc, level)	{};

	AbortClass(const char   *name,
	               Tango::CmdArgType in,
				   Tango::CmdArgType out)
	:Command(name,in,out)	{};
	~AbortClass() {};
	
	virtual CORBA::Any *execute (Tango::DeviceImpl *dev, const CORBA::Any &any);
	virtual bool is_allowed (Tango::DeviceImpl *dev, const CORBA::Any &any)
	{return (static_cast<CornerStone130 *>(dev))->is_Abort_allowed(any);}
};



//
// The CornerStone130Class singleton definition
//

class
#ifdef _TG_WINDOWS_
	__declspec(dllexport)
#endif
	CornerStone130Class : public Tango::DeviceClass
{
public:
//	properties member data

//	add your own data members here
//------------------------------------

public:
	Tango::DbData	cl_prop;
	Tango::DbData	cl_def_prop;
	Tango::DbData	dev_def_prop;

//	Method prototypes
	static CornerStone130Class *init(const char *);
	static CornerStone130Class *instance();
	~CornerStone130Class();
	Tango::DbDatum	get_class_property(string &);
	Tango::DbDatum	get_default_device_property(string &);
	Tango::DbDatum	get_default_class_property(string &);
	
protected:
	CornerStone130Class(string &);
	static CornerStone130Class *_instance;
	void command_factory();
	void get_class_property();
	void attribute_factory(vector<Tango::Attr *> &);
	void write_class_property();
	void set_default_property();
	string get_cvstag();
	string get_cvsroot();

private:
	void device_factory(const Tango::DevVarStringArray *);
};


}	//	namespace CornerStone130_ns

#endif // _CORNERSTONE130CLASS_H