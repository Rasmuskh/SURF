import ctypes

from numpy.ctypeslib import as_array

lib = ctypes.CDLL('/home/tango-cs/OmniDriver/OOI_HOME/libOmniDriver.so', mode = ctypes.RTLD_GLOBAL)#mode should make ctypes look for connected libraries

wrapperHandle = lib.Wrapper_Create()
import ctypes
from ctypes import *
from numpy.ctypeslib import as_array
import numpy as np


#open spectrometers and get number of spectrometers
def openAllSpectrometers(wrapperHandle):
	NumberOfSpectrometers=lib.Wrapper_openAllSpectrometers(wrapperHandle)
	if NumberOfSpectrometers==-1:
		raise exception('openAllSpectrometers returned -1. This means an I/O error has occurred')
	return NumberOfSpectrometers;

#get number of spectrometers. You must first call openAllSpectrometers().
def getNumberOfSpectrometersFound(wrapperHandle):
	N=lib.Wrapper_getNumberOfSpectrometersFound(wrapperHandle)
	return N;

#get the model name of the spectrometer
def getName(wrapperHandle, index, name):
	Name=lib.Wrapper_getName(wrapperHandle, index, name)
	return Name

def setIntegrationTime(wrapperHandle, spectrometerIndex, integrationtime):#time in microseconds.
	lib.Wrapper_setIntegrationTime(wrapperHandle, spectrometerIndex, integrationtime)
	return

def getSpectrum(wrapperHandle, spectrometerIndex):
	spectrum = lib.Wrapper_getSpectrum(wrapperHandle, spectrometerIndex)
	return spectrum

def closeAllSpectrometers(wrapperHandle):
	lib.Wrapper_closeAllSpectrometers(wrapperHandle)
	return

#-=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=-
#===,--,,-,_|_ ,--,,_
# | |--'`-, |  |--'|
# ' '--''-' '-''--'' 
#-=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=-
openAllSpectrometers.restype = ctypes.c_int  #ctypes.POINTER(ctypes.c_int)#should it be ctypes.c_int?????
#-=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=-
getNumberOfSpectrometersFound.restypes = ctypes.c_int
#-=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=-
getName.argtypes = [ctypes.c_int, ctypes.c_char]
getName.restype = ctypes.c_char #Is this the right datatype?
#-=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=-
setIntegrationTime.argtypes = [ctypes.c_int, ctypes.c_int]
#-=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=-
getSpectrum.argtypes = [ctypes.c_int, ctypes.c_int]
#getSpectrum.restype = ctypes.c_double*10 #Array#ctypes.POINTER(ctypes.c_float)#as_array()
#-=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=--=-=-
#Try out some functions!
#first instantiate the wrapperHandle
wrapperHandle = lib.Wrapper_Create()
N=openAllSpectrometers(wrapperHandle)
n=getNumberOfSpectrometersFound(wrapperHandle)
print('N = ', N, ' and n = ',n)
if n==N:
	print('both functions find the same numeber of spectrometers')
index=0
#name= ''
#Name0=getName(wrapperHandle, index,name)
#print(Name0)
setIntegrationTime(wrapperHandle,index,15)#integration time is in microseconds.
Spectrum = getSpectrum(wrapperHandle,index)
closeAllSpectrometers(wrapperHandle)

