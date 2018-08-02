import numpy
import PyTango
from PyTango import DispLevel, AttrWriteType, DevState#, Util, Attr, MultiAttrProp, AttrQuality, AttrWriteType, CmdArgType, UserDefaultAttrProp, DevState
from PyTango.server import DeviceMeta, Device, server_run
from PyTango.server import command, attribute

from PyOceansOpticsWrapper import OceansOpticsWrapper

class OceanOptics(Device):
    """Ocean Optics Spectrometer class"""

#Attributes
    __metaclass__ = DeviceMeta

    index = attribute(label = "index", unit = "", dtype = int,
                      display_level=DispLevel.EXPERT,
                      access = AttrWriteType.READ,
                      doc = "Spectrometer index")
    integrationTime = attribute(label = "Integration time",
                                display_level=DispLevel.OPERATOR,
                                unit = "micro seconds", dtype = int,
                                min_value = 0, access = AttrWriteType.READ_WRITE,
                                doc = "The Integration time used for acquiring the spectrum")

    darkCorrection = attribute(label = "Dark correction", unit = "",
                               display_level=DispLevel.OPERATOR,
                               dtype = int, access = AttrWriteType.READ_WRITE,
                               min_value = 0, max_value = 1,
                               doc = "electrical dark noise correction")
    strayLightCorrection = attribute(label = "Stray light correction", unit = "",
                                     display_level=DispLevel.OPERATOR,
                                     dtype = int, access = AttrWriteType.READ,
                                     min_value = 0, max_value = 1,
                                     doc = "Stray light correction")

    spectrum = attribute(label = "Spectrum", unit = "wavelength nm",
                         display_level=DispLevel.OPERATOR,
                       	 dtype=[int,],
                         max_dim_x=3645, max_dim_y=0,
                         access = AttrWriteType.READ,
                         doc = "Spectrum")

    scansToAverage = attribute(label = "Scans to average", unit = "", dtype = int,
                               min_value = 1, display_level=DispLevel.OPERATOR,
                               access = AttrWriteType.READ_WRITE,
                               doc = "Number of scans to average over")



    def init_device(self):
        Device.init_device(self)
        self.Spectrometer = OceansOpticsWrapper()
        self.set_state(PyTango.DevState.INIT)
        self.set_status("Device in init!")
        try:
            self.Spectrometer.__init__()
            self.Spectrometer.OpenSpectrometer('HR4C5720')
            self.index = self.read_index()
            self.integrationTime = self.read_integrationTime()
            self.darkCorrection = self.read_darkCorrection()
            self.scansToAverage = self.read_scansToAverage()
            self.set_state(PyTango.DevState.ON)
            self.set_status("Device is ON!")
            print("Device is now turned on")
        except Exception:
            print("Error Device could not initialize")
            self.set_state(DevState.FAULT)
            self.set_status("Device could not initialize!")

    def read_index(self):
        return self.Spectrometer.GetDeviceIndex()

    def read_integrationTime(self):
        if  self.Spectrometer.GetIntegrationTime() is not None:
            return self.Spectrometer.GetIntegrationTime()

    def write_integrationTime(self, T):
        self.Spectrometer.SetIntegrationTime(T)

    def read_darkCorrection(self):
        if self.Spectrometer.GetCorrectForElectricalDark() is not None:
            return self.Spectrometer.GetCorrectForElectricalDark()

    def write_darkCorrection(self, onoff):
        self.Spectrometer.SetCorrectForElectricalDark(onoff)

    def read_strayLightCorrection(self):
        return self.Spectrometer.GetCorrectForStrayLight()

    def read_spectrum(self):
        if self.integrationTime is not None:
            return self.Spectrometer.GetSpectrum()

    def read_scansToAverage(self):
        return self.Spectrometer.GetScansToAverage()

    def write_scansToAverage(self, number):
        self.Spectrometer.SetScansToAverage(number)

    def OpenSpectrometer(self):
        try:
            self.Spectrometer.OpenSpectrometer('HR4C5720')
        except Exception:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status("Failed to open spectrometer. Device is in fault!")

    @command
    def CloseSpectrometer(self):
        self.Spectrometer.CloseSpectrometer()
        self.set_state(PyTango.DevState.OFF)
        self.set_status("Device is OFF!")
    @command
    def StopAveraging(self):
        self.Spectrometer.StopAveraging()


if __name__ == "__main__":
    OceanOptics.run_server()
