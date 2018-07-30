# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 10:17:32 2018

@author: user
"""

from PyOceansOpticsWrapper import OceansOpticsWrapper

OO = OceansOpticsWrapper()
OO.__init__()
OO.OpenSpectrometer('HR4C5720')
print OO.GetSerialNumber()
print OO.GetName()
print OO.GetFirmwareVersion()
OO.SetIntegrationTime(4*1000)
print OO.GetIntegrationTime()
s = OO.GetSpectrum()
OO.CloseSpectrometer()
