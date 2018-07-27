#/**
# * File: PyOceansOpticsWrapper.py
# * Date: 2013-06-19
# * Description: Python wrapper class for the OMNIDRIVER of OceansOptics
# * Dependencies: OmniDriver64.dll and common64.dll 
# * Copyright (C) 2013 by Dr. Sylvio Haas.  All rights reserved.
# */

from ctypes import *
from array import array
import numpy as np
import sys
import os
import time

class OceansOpticsCoefficientsWrapper:
    """Wrapper class to the coefficient datatype of the OO dll."""
    
    def __init__(self, parent=None):
        """Constructor.
        @param parent parent widget of this class (default: None)
        """
        self.__loadLibraries()          # load libraries
        self.__redirectDllOutput()      # redirect stdout and stderr
        self.__createDllDataTypes()     # create datatypes in python 
        
    def GetNlCoef0(self):
        """Public method: get nonlinearity coefficient 0.
        @return value (double)
        """
        self.libOmniDriver.Coefficients_getNlCoef0.restype = c_double
        return self.libOmniDriver.Coefficients_getNlCoef0(self.dllCoefficients)
    
    def SetNlCoef0(self, value):
        """Public method: set nonlinearity coefficient 0.
        @param value nonlinearity coefficient 0
        @return none
        """
        self.libOmniDriver.Coefficients_setNlCoef0(self.dllCoefficients, c_double(value))
        return None
    
    def GetNlCoef1(self):
        """Public method: get nonlinearity coefficient 1.
        @return value (double)
        """
        self.libOmniDriver.Coefficients_getNlCoef1.restype = c_double
        return self.libOmniDriver.Coefficients_getNlCoef1(self.dllCoefficients)
    
    def SetNlCoef1(self, value):
        """Public method: set nonlinearity coefficient 1.
        @param value nonlinearity coefficient 1
        @return none
        """
        self.libOmniDriver.Coefficients_setNlCoef1(self.dllCoefficients, c_double(value))
        return None
    
    def GetNlCoef2(self):
        """Public method: get nonlinearity coefficient 2.
        @return value (double)
        """
        self.libOmniDriver.Coefficients_getNlCoef2.restype = c_double
        return self.libOmniDriver.Coefficients_getNlCoef2(self.dllCoefficients)

    def SetNlCoef2(self, value):
        """Public method: set nonlinearity coefficient 2.
        @param value nonlinearity coefficient 2
        @return none
        """
        self.libOmniDriver.Coefficients_setNlCoef2(self.dllCoefficients, c_double(value))
        return None

    def GetNlCoef3(self):
        """Public method: get nonlinearity coefficient 3.
        @return value (double)
        """
        self.libOmniDriver.Coefficients_getNlCoef3.restype = c_double
        return self.libOmniDriver.Coefficients_getNlCoef3(self.dllCoefficients)
    
    def SetNlCoef3(self, value):
        """Public method: set nonlinearity coefficient 3.
        @param value nonlinearity coefficient 3
        @return none
        """
        self.libOmniDriver.Coefficients_setNlCoef3(self.dllCoefficients, c_double(value))
        return None
    
    def GetNlCoef4(self):
        """Public method: get nonlinearity coefficient 4.
        @return value (double)
        """
        self.libOmniDriver.Coefficients_getNlCoef4.restype = c_double
        return self.libOmniDriver.Coefficients_getNlCoef4(self.dllCoefficients)
  
    def SetNlCoef4(self, value):
        """Public method: set nonlinearity coefficient 4.
        @param value nonlinearity coefficient 4
        @return none
        """
        self.libOmniDriver.Coefficients_setNlCoef4(self.dllCoefficients, c_double(value))
        return None
   
    def GetNlCoef5(self):
        """Public method: get nonlinearity coefficient 5.
        @return value (double)
        """
        self.libOmniDriver.Coefficients_getNlCoef5.restype = c_double
        return self.libOmniDriver.Coefficients_getNlCoef5(self.dllCoefficients)
    
    def SetNlCoef5(self, value):
        """Public method: set nonlinearity coefficient 5.
        @param value nonlinearity coefficient 5
        @return none
        """
        self.libOmniDriver.Coefficients_setNlCoef5(self.dllCoefficients, c_double(value))
        return None
    
    def GetNlCoef6(self):
        """Public method: get nonlinearity coefficient 6.
        @return value (double)
        """
        self.libOmniDriver.Coefficients_getNlCoef6.restype = c_double
        return self.libOmniDriver.Coefficients_getNlCoef6(self.dllCoefficients)
    
    def SetNlCoef6(self, value):
        """Public method: set nonlinearity coefficient 6.
        @param value nonlinearity coefficient 6
        @return none
        """
        self.libOmniDriver.Coefficients_setNlCoef6(self.dllCoefficients, c_double(value))
        return None
    
    def GetNlCoef7(self):
        """Public method: get nonlinearity coefficient 7.
        @return value (double)
        """
        self.libOmniDriver.Coefficients_getNlCoef7.restype = c_double
        return self.libOmniDriver.Coefficients_getNlCoef7(self.dllCoefficients)
    
    def SetNlCoef7(self, value):
        """Public method: set nonlinearity coefficient 7.
        @param value nonlinearity coefficient 7
        @return none
        """
        self.libOmniDriver.Coefficients_setNlCoef7(self.dllCoefficients, c_double(value))
        return None
    
    def GetNlCoef(self):
        """Public method: get nonlinearity coefficients.
        @return coefficients (numpy array)
        """
        return np.array([self.GetNlCoef0(), 
                         self.GetNlCoef1(),
                         self.GetNlCoef2(),
                         self.GetNlCoef3(),
                         self.GetNlCoef4(), 
                         self.GetNlCoef5(),
                         self.GetNlCoef6(),
                         self.GetNlCoef7()])
    
    def SetNlCoef(self, values):
        """Public method: set nonlinearity coefficients.
        @param values nonlinearity coefficients (numpy array length 8)
        @return none
        """
        try:
            self.SetNlCoef0(values[0])
            self.SetNlCoef1(values[1])
            self.SetNlCoef2(values[2])
            self.SetNlCoef3(values[3])
            self.SetNlCoef4(values[4])
            self.SetNlCoef5(values[5])
            self.SetNlCoef6(values[6])
            self.SetNlCoef7(values[7])
        except IndexError:
            pass
        return None
    
    def GetNlOrder(self):
        """Public method: get nonlinearity polynom order.
        @return polynom order (int)
        """
        self.libOmniDriver.Coefficients_getNlOrder.restype = c_int
        return self.libOmniDriver.Coefficients_getNlOrder(self.dllCoefficients)

    def SetNlOrder(self, value):
        """Public method: set nonlinearity polynom order.
        @param value polynom order (1-7)
        @return none
        """
        self.libOmniDriver.Coefficients_setNlOrder(self.dllCoefficients, c_int(value))
        return None

    def GetWlIntercept(self):
        """Public method: get wavelength intercept.
        @return wavelength intercept (double)
        """
        self.libOmniDriver.Coefficients_getWlIntercept.restype = c_double
        return self.libOmniDriver.Coefficients_getWlIntercept(self.dllCoefficients)
    
    def SetWlIntercept(self, value):
        """Public method: set wavelength intercept.
        @param value wavelength intercept
        @return none
        """
        self.libOmniDriver.Coefficients_setWlIntercept(self.dllCoefficients, c_double(value))
        return None
    
    def GetWlFirst(self):
        """Public method: get wavelength first order coefficient.
        @return wavelength first coef (double)
        """
        self.libOmniDriver.Coefficients_getWlFirst.restype = c_double
        return self.libOmniDriver.Coefficients_getWlFirst(self.dllCoefficients)

    def SetWlFirst(self, value):
        """Public method: set wavelength first order coefficient.
        @param value wavelength first order coefficient
        @return none
        """
        self.libOmniDriver.Coefficients_setWlFirst(self.dllCoefficients, c_double(value))
        return None
    
    def GetWlSecond(self):
        """Public method: get wavelength second order coefficient.
        @return wavelength second coef (double)
        """
        self.libOmniDriver.Coefficients_getWlSecond.restype = c_double
        return self.libOmniDriver.Coefficients_getWlSecond(self.dllCoefficients)

    def SetWlSecond(self, value):
        """Public method: set wavelength second order coefficient.
        @param value wavelength second order coefficient
        @return none
        """
        self.libOmniDriver.Coefficients_setWlSecond(self.dllCoefficients, c_double(value))
        return None
    
    def GetWlThird(self):
        """Public method: get wavelength third order coefficient.
        @return wavelength third coef (double)
        """
        self.libOmniDriver.Coefficients_getWlThird.restype = c_double
        return self.libOmniDriver.Coefficients_getWlThird(self.dllCoefficients)
    
    def SetWlThird(self, value):
        """Public method: set wavelength third order coefficient.
        @param value wavelength third order coefficient
        @return none
        """
        self.libOmniDriver.Coefficients_setWlThird(self.dllCoefficients, c_double(value))
        return None
    
    def GetWlCoef(self):
        """Public method: get wavelength coefficients.
        @return coefficients (numpy array)
        """
        return np.array([self.GetWlIntercept(),
                         self.GetWlFirst(), 
                         self.GetWlSecond(), 
                         self.GetWlThird()])    
    
    def SetWlCoef(self, values):
        """Public method: set wavelength coefficients.
        @param values Wavelenngth coefficients (numpy array length 4)
        @return none
        """
        try:
            self.SetWlIntercept(values[0])
            self.SetWlFirst(values[1])
            self.SetWlSecond(values[2])
            self.SetWlThird(values[3])
        except IndexError:
            pass
        return None
    
    def GetStrayLight(self):
        """Public method: get stray light value.
        @return stray light value (double)
        """
        self.libOmniDriver.Coefficients_getStrayLight.restype = c_double
        return self.libOmniDriver.Coefficients_getStrayLight(self.dllCoefficients)
    
    def SetStrayLight(self, value):
        """Public method: set stray light coefficient.
        @param value Stray light coefficient
        @return none
        """
        self.libOmniDriver.Coefficients_setStrayLight(self.dllCoefficients, c_double(value))
        return None
    
    
    def __createDllDataTypes(self):
        """Private method: create the ctypes objects for the dll datatypes.
        @return none
        """
        self.dllCoefficients = self.libOmniDriver.Coefficients_Create()
        
    def __loadLibraries(self):
        """Private method: load the common library.
        @return library object (pointer to OmniDriver64.dll)
        """
        self.libOmniDriver = cdll.LoadLibrary('/home/tango-cs/OmniDriverSPAM/OOI_HOME/libOmniDriver.so')
        return self.libOmniDriver
    
    def __redirectDllOutput(self):
        """Private method: redirect the dll stdout and stderr to a log file (only windows).
        @return none
        """
        if os.name == 'nt':
            import msvcrt
            k32 = windll.kernel32
            fstdout = open("tmp_stdout_dll.log", 'w')
            fstderr = open("tmp_stderr_dll.log", 'w')
            k32.SetStdHandle(-11, msvcrt.get_osfhandle(fstdout.fileno()))
            k32.SetStdHandle(-12, msvcrt.get_osfhandle(fstderr.fileno()))




class OceansOpticsWrapper:
    """Wrapper class to communicate with Oceans Optics Spectrometers.""" 
        
    def __init__(self, parent=None):
        """Constructor.
        @param parent parent widget of this class (default: None)
        """
        self.nrOfPixels = -1            # number of pixels
        self.__loadLibraries()          # load libraries
        self.__redirectDllOutput()      # redirect stdout and stderr
        self.__createDllDataTypes()     # create datatypes in python 
        self.coefficients = OceansOpticsCoefficientsWrapper()
    
    def GetCalibrationCoefficientsFromBuffer(self,  index= None):
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return None
        self.libOmniDriver.Wrapper_getCalibrationCoefficientsFromBuffer(self.dllWrapper, c_int(index), self.coefficients.dllCoefficients)
        
    
    def GetDeviceIndex(self):
        """Public method: device index variable.
        @return current device index (int)
        """
        return self.deviceIndex
    
    def GetNrDevicesFound(self):
        """Public method: number of OceansOptics devices connected to the computer.
        @return number of devices found (int)
        """
        return self.nrDevicesFound
    
    def OpenSpectrometer(self, serialnumber):
        """Public method: open spectrometer with a known serialnumber. 
        @param serialnumber Serialnumber of the spectrometer to open (string)
        @return None
        """
        self.deviceIndex = -1          
        self.nrDevicesFound = -1
        self.__openAllSpectrometers()
        if self.nrDevicesFound == 0:
            print "OceansOptics::No spectrometer found!"
            return
        # get the serial number of all spectrometers
        for i in range(1, self.nrDevicesFound+1):
            index = i -1
            print 'checking device index: %d - %s'%(index, self.GetSerialNumber(index))
            if self.GetSerialNumber(index)==serialnumber:
                self.deviceIndex = index
            else:
                self.libOmniDriver.Wrapper_closeSpectrometer(self.dllWrapper, c_int(index))
                    
        print 'Device index: %d'%self.deviceIndex
        if self.deviceIndex == -1:
            print "OceansOptics::No spectrometer with serial number < ",str(serialnumber)," > found!"
        return

    def CloseSpectrometer(self,  index=None):
        """Public method: close the current spectrometer.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @returns none
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return None
        # the close command does not work correctly with python's ctype
        self.libOmniDriver.Wrapper_closeSpectrometer(self.dllWrapper, c_int(index))
        print 'closing spectrometer: %d'%self.deviceIndex
        self.deviceIndex = -1

    def GetSerialNumber(self, index=None):
        """Public method: get the serial number of the device.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return serial number (string)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return None
        try:
            self.libOmniDriver.Wrapper_getSerialNumber(self.dllWrapper, c_int(index), self.dllJString)
        except:
            pass
        return self.__JStringToStr()
        
    def GetName(self, index=None):
        """Public method: get the name of the device.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return name (string)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return None
        self.libOmniDriver.Wrapper_getName(self.dllWrapper, c_int(index), self.dllJString)
        return self.__JStringToStr()
    
    def GetFirmwareVersion(self, index=None):
        """Public method: get the firmware version.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return firmware version (string)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return None
        self.libOmniDriver.Wrapper_getFirmwareVersion(self.dllWrapper, c_int(index), self.dllJString)
        return self.__JStringToStr()
    
    def GetWavelengths(self, index=None):
        """Public method: get the calibrated wavelengths from the device.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return wavelengts array (numpy 1D array of float)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return None
        self.GetNumberOfPixels(index)
        self.libOmniDriver.Wrapper_getWavelengths(self.dllWrapper, c_int(index), self.dllDoubleArray)
        return self.__DoubleArrayToArray()
    
    def GetSpectrum(self,  index=None):
        """Public method: get the current spectrum intensities.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return intensities array (numpy 1D array of float)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return None
        self.GetNumberOfPixels(index)
        tstart = time.clock()
        self.libOmniDriver.Wrapper_getSpectrum(self.dllWrapper, c_int(index), self.dllDoubleArray)
        tend = time.clock()
        print "%.4gs" % (tend-tstart)
        return self.__DoubleArrayToArray()
    
    def GetNumberOfPixels(self, index = None):
        """Public method: get number of pixels from class attribute.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return number of pixels (int)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return None
        if self.nrOfPixels == -1:
            self.nrOfPixels = self.GetNumberOfPixelsDevice(index)
        return self.nrOfPixels
        
    def GetNumberOfPixelsDevice(self,  index = None):
        """Public method: get the number of pixels from the device epprom.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return number of pixels (int)"""
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return None
        self.nrOfPixels = int(self.libOmniDriver.Wrapper_getNumberOfPixels(self.dllWrapper, c_int(index)))
        return self.nrOfPixels
    
    def GetCorrectForElectricalDark(self, index=None):
        """Public method: get status of electronic dark correction.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return status on == 1 and off == 0(short)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return None
        self.libOmniDriver.Wrapper_getCorrectForElectricalDark.restype = c_short
        return self.libOmniDriver.Wrapper_getCorrectForElectricalDark(self.dllWrapper, c_int(index))
    
    def SetCorrectForElectricalDark(self, enable, index=None):
        """Public method: set the electronic dark compenstion on/off.
        @param enable Switch the correction on == 1 or off == 0
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return none
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return None
        self.libOmniDriver.Wrapper_setCorrectForElectricalDark(self.dllWrapper, c_int(index), c_int(enable))
    
    def GetCorrectForStrayLight(self, index=None):
        """Public method: get status of stray light correctin.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return status on == 1 and off == 0(short)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return None
        self.libOmniDriver.Wrapper_getCorrectForStrayLight.restype = c_short
        return self.libOmniDriver.Wrapper_getCorrectForStrayLight(self.dllWrapper, c_int(index))
 
    def GetCorrectForDetectorNonlinearity(self, index=None):
        """Public method: get status of detector nonlinearity correction.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return status on == 1 and off == 0 (short)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return None
        self.libOmniDriver.Wrapper_getCorrectForDetectorNonlinearity.restype = c_short
        return self.libOmniDriver.Wrapper_getCorrectForDetectorNonlinearity(self.dllWrapper, c_int(index))
    
    def SetCorrectForDetectorNonlinearity(self, enable, index=None):
        """Public method: set the detector nonlineartity correction on/off.
        @param enable Switch the correction on == 1 or off == 0
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return none"""
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return None
        self.libOmniDriver.Wrapper_setCorrectForDetectorNonlinearity(self.dllWrapper, c_int(index), c_int(enable))
   
    def GetIntegrationTime(self, index=None):
        """Public method: get the current integration time from the device.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return integration time usec (int)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return None
        self.libOmniDriver.Wrapper_getIntegrationTime.restype = c_int
        return self.libOmniDriver.Wrapper_getIntegrationTime(self.dllWrapper, c_int(index))
    
    def SetIntegrationTime(self, usec, index=None):
        """Public method: set the integration time usec.
        @param usec integration time in usec
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return none
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return None
        self.libOmniDriver.Wrapper_setIntegrationTime(self.dllWrapper, c_int(index), c_int(usec))
   
    def GetScansToAverage(self, index=None):
        """Public method: get number of scans to average.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return number of scans (int)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return -1
        self.libOmniDriver.Wrapper_getScansToAverage.restype = c_int
        return self.libOmniDriver.Wrapper_getScansToAverage(self.dllWrapper, c_int(index))
      
    def SetScansToAverage(self, number,  index=None):
        """Public method: set number of scans to average.
        @param number number of scans to average
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return none
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return None
        self.libOmniDriver.Wrapper_setScansToAverage(self.dllWrapper, c_int(index), c_int(number))
        return None
    
    def GetMinimumIntegrationTime(self, index=None):
        """Public method: get minimum integration time in usec.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return minimum integration time in usec (int)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return -1
        self.libOmniDriver.Wrapper_getMinimumIntegrationTime.restype = c_int
        return self.libOmniDriver.Wrapper_getMinimumIntegrationTime(self.dllWrapper, c_int(index))

    def GetMaximumIntegrationTime(self, index=None):
        """Public method: get maximum integration time in usec.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return maximum integration time in usec (int)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return -1
        self.libOmniDriver.Wrapper_getMaximumIntegrationTime.restype = c_int
        return self.libOmniDriver.Wrapper_getMaximumIntegrationTime(self.dllWrapper, c_int(index))

    def GetMaximumIntensity(self, index):
        """Public method: get maximum intensity of device.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return maximum intensity (int)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return -1
        self.libOmniDriver.Wrapper_getMaximumIntensity.restype = c_int
        return self.libOmniDriver.Wrapper_getMaximumIntensity(self.dllWrapper, c_int(index))

    def IsSaturated(self, index=None):
        """Public method: check if detector is saturated.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return status of staturation  no == 0 or yes == 1(short)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return -1
        self.libOmniDriver.Wrapper_isSaturated.restype = c_short
        return self.libOmniDriver.Wrapper_isSaturated(self.dllWrapper, c_int(index))

    def IsTimeout(self, index=None):
        """Public method: check for timeout.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return status of timeout  no == 0 or yes == 1(short)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return -1
        self.libOmniDriver.Wrapper_isTimeout.restype = c_short
        return self.libOmniDriver.Wrapper_isTimeout(self.dllWrapper, c_int(index))

    def SetTimeout(self, msec, index=None):
        """Public method: set timeout in msec of the device.
        @param msec timeout in msec of the device
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return timeout (int)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return -1
        self.libOmniDriver.Wrapper_setTimeout.restype = c_int
        return self.libOmniDriver.Wrapper_setTimeout(self.dllWrapper, c_int(index), c_int(msec))

    def IsSpectrumValid(self, index=None):
        """Public method: check if spectrum is valid.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return status of spectrum validity  no == 0 or yes == 1(short)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return -1
        self.libOmniDriver.Wrapper_isSpectrumValid.restype = c_short
        return self.libOmniDriver.Wrapper_isSpectrumValid(self.dllWrapper, c_int(index))

    def StopAveraging(self, index=None):
        """Public method: stop the averaging process.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return none
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return None
        self.libOmniDriver.Wrapper_stopAveraging(self.dllWrapper, c_int(index))

    def FlushSpectrum(self, index=None):
        """Public method: flush the current spectrum.
        @param index optional: device index of the spectrometer (default: None == self.deviceIndex value)
        @return status of flush  no == 0 or yes == 1(short)
        """
        if index == None:
            index = self.deviceIndex
        if index == -1:
            return -1
        self.libOmniDriver.Wrapper_flushSpectrum.restype = c_short
        return self.libOmniDriver.Wrapper_flushSpectrum(self.dllWrapper, c_int(index))


    def __DoubleArrayToArray(self, arrIn=None):
        """Private method: convert OO_DoubleArray to numpy array object.
        @param arrIn Array object to convert (default: None == uses the class object self.dllDoubleArray
        @return numpy array object of arrIN
        """
        if arrIn == None:
            arrIn = self.dllDoubleArray
        self.libCommon.DoubleArray_getDoubleValues.restype = POINTER(c_double * int(self.nrOfPixels))
        pArr = self.libCommon.DoubleArray_getDoubleValues(arrIn)
        value = np.array(list(pArr.contents))
        return np.delete(value, [0, 1, 2], axis=0)

    def __JStringToStr(self, jstr=None):
        """Private method: convert OO_JString to python string.
        @param jstr JString object to convert (default: None == uses the class object self.dllJString
        @return python string of jstr
        """
        if jstr == None:
            jstr= self.dllJString
        text = c_char_p(self.libCommon.JString_getASCII(jstr))
        return str(text.value)

    def __openAllSpectrometers(self):
        """Private method: open all Spectrometers connected to the computer.
        @return none
        """
        try:
            self.libOmniDriver.Wrapper_openAllSpectrometers.restype = c_int
            self.nrDevicesFound = self.libOmniDriver.Wrapper_openAllSpectrometers(self.dllWrapper)
        except:
            self.nrDevicesFound = 0
    
    def __createDllDataTypes(self):
        """Private method: create the ctypes objects for the dll datatypes.
        @return none
        """
        self.dllWrapper = c_void_p(self.libOmniDriver.Wrapper_Create())
        self.dllJString = self.libCommon.JString_Create()
        self.dllDoubleArray = c_void_p(self.libCommon.DoubleArray_Create())
        
    def __loadLibraries(self):
        """Private method: load the OO libraries.
        @return none
        """
        self.libOmniDriver = cdll.LoadLibrary('/home/tango-cs/OmniDriverSPAM/OOI_HOME/libOmniDriver.so')
        self.libCommon = cdll.LoadLibrary('/home/tango-cs/OmniDriverSPAM/OOI_HOME/libcommon.so')
    
    def __redirectDllOutput(self):
        """Private method: redirect the dll stdout and stderr to a log file (only windows).
        @return none
        """
        if os.name == 'nt':
            import msvcrt
            k32 = windll.kernel32
            fstdout = open("tmp_stdout_dll.log", 'w')
            fstderr = open("tmp_stderr_dll.log", 'w')
            k32.SetStdHandle(-11, msvcrt.get_osfhandle(fstdout.fileno()))
            k32.SetStdHandle(-12, msvcrt.get_osfhandle(fstderr.fileno()))


