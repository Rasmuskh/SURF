import numpy
import PyTango
from PyTango import Util, Attr, MultiAttrProp, AttrQuality, AttrWriteType, CmdArgType, UserDefaultAttrProp, DevState
from PyTango.server import DeviceMeta, Device, server_run
from PyTango.server import command, attribute

from PyOceansOpticsWrapper import OceansOpticsWrapper

class OceanOptics(Device):
    """Ocean Optics Spectrometer class"""

#Attributes
    __metaclass__ = DeviceMeta

    index = attribute(label = "index", unit = "", dtype = int,
                      access = AttrWriteType.READ,
                      doc = "Spectrometer index")

    darkCorrection = attribute(label = "Dark correction", unit = "",
                               dtype = int,
                               access = AttrWriteType.READ,
                               doc = "electrical dark noise correction")

    spectrum = attribute(label = "Spectrum", unit = "wavelength nm",
                       	 dtype=[int,],
                         max_dim_x=3645, max_dim_y=0,
                         access = AttrWriteType.READ,
                         doc = "Spectrum")



    def init_device(self):
        Device.init_device(self)
        self.Spectrometer = OceansOpticsWrapper()
        self.set_state(PyTango.DevState.INIT)
        self.set_status("Device in init!")
        try:
            self.Spectrometer.__init__()
            self.Spectrometer.OpenSpectrometer('HR4C5720')
        except OceanOpticsException:
            print("Error")
            self.set_state(DevState.FAULT)
            self.set_status("Device could not initialize!")
        self.index = self.read_index()
        self.darkCorrection = self.read_darkCorrection()
        self.spectrum = self.read_spectrum()
        self.set_state(PyTango.DevState.ON)
        self.set_status("Device is ON!")

    def read_index(self):
        return self.Spectrometer.GetDeviceIndex()
    def read_darkCorrection(self):
        try:
            return self.Spectrometer.GetCorrectForElectricalDark()
        except OceanOpticsException:
            print("Error")
            self.set_status("Device could not acquire dark correction")
    def read_spectrum(self):
        return self.Spectrometer.GetSpectrum()
   

    


    @command
    def OpenSpectrometer(self):
        self.Spectrometer.OpenSpectrometer('HR4C5720')
        self.set_state(PyTango.DevState.ON)
        self.set_status("Device is ON!")

    @command
    def CloseSpectrometer(self):
        self.Spectrometer.CloseSpectrometer()
        self.set_state(PyTango.DevState.OFF)
        self.set_status("Device is OFF!")



if __name__ == "__main__":
    OceanOptics.run_server()
