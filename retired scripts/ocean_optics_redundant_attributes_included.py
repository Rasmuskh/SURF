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

    nonLinearityCorrection = attribute(label = "Nonlinearity correction", unit = "",
                               display_level=DispLevel.OPERATOR,
                               dtype = int, access = AttrWriteType.READ_WRITE,
                               min_value = 0, max_value = 1,
                               doc = "Nonlinearity correction")

    strayLightCorrection = attribute(label = "Stray light correction", unit = "",
                                     display_level=DispLevel.OPERATOR,
                                     dtype = int, access = AttrWriteType.READ,
                                     min_value = 0, max_value = 1,
                                     doc = "Stray light correction")

    isSpectrumValid = attribute(label = "Is spectrum Valid?", unit = "",
                                display_level=DispLevel.EXPERT,
                                dtype = int, access = AttrWriteType.READ,
                                min_value = 0, max_value = 1,
                                doc = "Reads if spectrum is valid")

    isSaturated = attribute(label = "is spectrum saturated?", unit = "",
                                display_level=DispLevel.EXPERT,
                                dtype = int, access = AttrWriteType.READ,
                                min_value = 0, max_value = 1,
                                doc = "Reads if spectrum is saturated")

    TimeoutDuration = attribute(label = "Timeout", unit = "miliseconds",
                                display_level=DispLevel.EXPERT,
                                dtype = int, access = AttrWriteType.WRITE,
                                min_value = 0,
                                doc = "Timeout in miliseconds")

    isTimeoutOn = attribute(label = "is Timeout On", unit = "",
                            display_level=DispLevel.EXPERT,
                            dtype = bool, access = AttrWriteType.READ,
                            doc = "Tells wether timeout is being applied or not.")



    scansToAverage = attribute(label = "Scans to average", unit = "", dtype = int,
                               min_value = 1, display_level=DispLevel.OPERATOR,
                               access = AttrWriteType.READ_WRITE,
                               doc = "Number of scans to average over")

    minIntegrationTime = attribute(label = "Minimum integration time",
                                   unit = "micro seconds", dtype = int,
                                   display_level=DispLevel.EXPERT,
                                   access = AttrWriteType.READ,
                                   doc = "Minimum integration time")

    maxIntegrationTime = attribute(label = "Maximum integration time",
                                   unit = "micro seconds", dtype = int,
                                   display_level=DispLevel.EXPERT,
                                   access = AttrWriteType.READ,
                                   doc = "Maximum integration time")

    maxIntensity = attribute(label = "Maximum intensity", unit = "micro seconds", dtype = int,
                                   display_level=DispLevel.EXPERT,
                                   access = AttrWriteType.READ,
                                   doc = "Maximum intensity")

    spectrum = attribute(label = "Spectrum", unit = "",
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

    def OpenSpectrometer(self):
        try:
            self.Spectrometer.OpenSpectrometer('HR4C5720')
        except Exception:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status("Failed to open spectrometer. Device is in fault!")

    def read_index(self):
        return self.Spectrometer.GetDeviceIndex()

    def read_integrationTime(self):
        return self.Spectrometer.GetIntegrationTime()

    def write_integrationTime(self, T):
        self.Spectrometer.SetIntegrationTime(T)

    def read_darkCorrection(self):
        return self.Spectrometer.GetCorrectForElectricalDark()

    def write_darkCorrection(self, onoff):
        self.Spectrometer.SetCorrectForElectricalDark(onoff)

    def read_nonLinearityCorrection(self):
        return self.Spectrometer.GetCorrectForDetectorNonlinearity()

    def write_nonLinearityCorrection(self, onoff):
        self.Spectrometer.SetCorrectForDetectorNonlinearity(onoff)

    def read_strayLightCorrection(self):
        return self.Spectrometer.GetCorrectForStrayLight()



    def read_scansToAverage(self):
        return self.Spectrometer.GetScansToAverage()

    def write_scansToAverage(self, number):
        self.Spectrometer.SetScansToAverage(number)

    def read_minIntegrationTime(self):
        return self.Spectrometer.GetMinimumIntegrationTime()

    def read_maxIntegrationTime(self):
        return self.Spectrometer.GetMinimumIntegrationTime()

    def read_maxIntensity(self):
        return self.Spectrometer.GetMaximumIntensity()

    def read_isSpectrumValid(self):
        return self.Spectrometer.IsSpectrumValid()

    def read_isSaturated(self):
        return self.Spectrometer.IsSaturated()

    def read_isTimeoutOn(self):
        return self.Spectrometer.IsTimeout()

    def write_TimeoutDuration(self, msec):
        self.Spectrometer.IsTimeout(msec)

    def read_spectrum(self):
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
    OceanOptics.run_server()
