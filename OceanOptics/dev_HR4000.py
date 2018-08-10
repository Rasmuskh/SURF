import numpy
import PyTango
from PyTango import DispLevel, AttrWriteType, DevState
from PyTango.server import DeviceMeta, Device, server_run
from PyTango.server import command, attribute, device_property

from PyOceansOpticsWrapper import OceansOpticsWrapper

class HR4000(Device):
    """Ocean Optics Spectrometer class"""

    __metaclass__ = DeviceMeta
    #properties
    serial_port = device_property(dtype = str, default_value= "HR4C5720")

    #Attributes
    Index = attribute(label = "index", unit = "", dtype = int,
                      display_level=DispLevel.EXPERT,
                      access = AttrWriteType.READ,
                      doc = "Spectrometer index")

    IntegrationTime = attribute(label = "Integration time",
                                display_level=DispLevel.OPERATOR,
                                unit = "micro seconds", dtype = int,
                                min_value = 0, access = AttrWriteType.READ_WRITE,
                                doc = "The Integration time used for acquiring the spectrum")

    DarkCorrection = attribute(label = "Dark correction", unit = "",
                               display_level=DispLevel.OPERATOR,
                               dtype = bool, access = AttrWriteType.READ_WRITE,
                               doc = "electrical dark noise correction")

    NonLinearityCorrection = attribute(label = "Nonlinearity correction", unit = "",
                               display_level=DispLevel.OPERATOR,
                               dtype = bool, access = AttrWriteType.READ_WRITE,
                               doc = "Nonlinearity correction")

    StrayLightCorrection = attribute(label = "Stray light correction", unit = "",
                                     display_level=DispLevel.OPERATOR,
                                     dtype = bool, access = AttrWriteType.READ,
                                     doc = "Stray light correction")

    IsSpectrumValid = attribute(label = "Is spectrum Valid?", unit = "",
                                display_level=DispLevel.EXPERT,
                                dtype = int, access = AttrWriteType.READ,
                                min_value = 0, max_value = 1,
                                doc = "Reads if spectrum is valid")

    IsSaturated = attribute(label = "is spectrum saturated?", unit = "",
                                display_level=DispLevel.EXPERT,
                                dtype = int, access = AttrWriteType.READ,
                                min_value = 0, max_value = 1,
                                doc = "Reads if spectrum is saturated")




    ScansToAverage = attribute(label = "Scans to average", unit = "", dtype = int,
                               min_value = 1, display_level=DispLevel.OPERATOR,
                               access = AttrWriteType.READ_WRITE,
                               doc = "Number of scans to average over")


    Spectrum = attribute(label = "Spectrum", unit = "",
                         display_level=DispLevel.OPERATOR,
                       	 dtype=[int,],
                         max_dim_x=3645, max_dim_y=0,
                         access = AttrWriteType.READ,
                         doc = "Spectrum: X-axis:pixel number, Y-axis: pixel value. Use Wavelengths() function to get the wavelengths corresponding to the pixel values.")

    Wavelengths = attribute(label = "Wavelengths", unit = "nm",
                            display_level=DispLevel.OPERATOR,
                       	    dtype=[float,],
                            max_dim_x=3645, max_dim_y=0,
                            access = AttrWriteType.READ,
                            doc = "Wavelengths of each pixel in the most recently acquired spectrum spectrum.")

    CalibrationCoefficients = attribute(label = "Calibration coefficients",
                                        display_level=DispLevel.EXPERT,
                       	                dtype=[float,],
                                        max_dim_x=4, max_dim_y=0,
                                        access = AttrWriteType.READ,
                                        doc = "Read the callibration coefficients, used for converting pixel values into wavelengths, from the spectrometers buffer.")



    def init_device(self):
        Device.init_device(self)
        self.Spectrometer = OceansOpticsWrapper()
        self.set_state(PyTango.DevState.INIT)
        self.set_status("Device in init!")
        try:
            self.Spectrometer.__init__()
            self.Spectrometer.OpenSpectrometer(self.serial_port)
            self.set_state(PyTango.DevState.ON)
            self.set_status("Device is ON!")
            print("Device is now turned on")
        except Exception:
            print("Error Device could not initialize")
            self.set_state(DevState.FAULT)
            self.set_status("Device could not initialize!")


    def read_Index(self):
        return self.Spectrometer.GetDeviceIndex()

    def read_IntegrationTime(self):
        return self.Spectrometer.GetIntegrationTime()

    def write_IntegrationTime(self, T):
        self.Spectrometer.SetIntegrationTime(T)

    def read_DarkCorrection(self):
        return bool(self.Spectrometer.GetCorrectForElectricalDark())

    def write_DarkCorrection(self, onoff):
        self.Spectrometer.SetCorrectForElectricalDark(onoff)

    def read_NonLinearityCorrection(self):
        return bool(self.Spectrometer.GetCorrectForDetectorNonlinearity())

    def write_NonLinearityCorrection(self, onoff):
        self.Spectrometer.SetCorrectForDetectorNonlinearity(onoff)

    def read_StrayLightCorrection(self):
        return bool(self.Spectrometer.GetCorrectForStrayLight())



    def read_ScansToAverage(self):
        return self.Spectrometer.GetScansToAverage()

    def write_ScansToAverage(self, number):
        self.Spectrometer.SetScansToAverage(number)




    def read_IsSpectrumValid(self):
        return self.Spectrometer.IsSpectrumValid()

    def read_IsSaturated(self):
        return self.Spectrometer.IsSaturated()

   

    def read_Spectrum(self):
        return self.Spectrometer.GetSpectrum()

    def read_Wavelengths(self):
        return self.Spectrometer.GetWavelengths()

    def read_CalibrationCoefficients(self):
        return self.Spectrometer.GetCalibrationCoefficientsFromBuffer()




    @command
    def CloseSpectrometer(self):
        self.Spectrometer.CloseSpectrometer()
        self.set_state(PyTango.DevState.OFF)
        self.set_status("Device is OFF!")
    @command
    def StopAveraging(self):
        self.Spectrometer.StopAveraging()


if __name__ == "__main__":
    HR4000.run_server()
