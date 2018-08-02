# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 10:17:32 2018

@author: user
"""
import matplotlib.pyplot as plt
from PyOceansOpticsWrapper import OceansOpticsWrapper

OO = OceansOpticsWrapper()
OO.__init__()
OO.OpenSpectrometer('HR4C5720')
print OO.GetSerialNumber()
print OO.GetName()
print OO.GetDeviceIndex()
print OO.GetFirmwareVersion()
print OO.GetCorrectForElectricalDark()
OO.SetIntegrationTime(4*1000)
print OO.GetIntegrationTime()
d = OO.GetCorrectForElectricalDark()
s = OO.GetSpectrum()
#plt.plot(s)
#plt.show()
OO.CloseSpectrometer()
