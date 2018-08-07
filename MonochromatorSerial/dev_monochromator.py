import numpy
import PyTango
from PyTango import DispLevel, AttrWriteType, DevState
from PyTango.server import DeviceMeta, Device, server_run
from PyTango.server import command, attribute, device_property

import lib_monochromator as lm

class Cornerstone(Device):
    __metaclass__ = DeviceMeta
    #properties
    serial_port = device_property(dtype = str, default_value= "/dev/ttyUSB0")

    #attributes
    Wavelength = attribute(label = "Wavelength", unit ="nm",
                           display_level=DispLevel.OPERATOR,
                           min_value = 0, max_value = 1600,
                           dtype = int, access = AttrWriteType.READ_WRITE,
                           doc = "Choose the wavelength the monochromator lets through.")

    #step
    #grating
    #shutter = attribute(label = "Shutter status", unit = "",
    #                    display_level=DispLevel.OPERATOR,
    #                    dtype = str, access = AttrWriteType.READ,
    #                    doc = "Shutter can be either open or closed.")


    def init_device(self):
        Device.init_device(self)
        #self.Monochromator = Mono(self.serial_port)
        self.set_state(PyTango.DevState.INIT)
        self.set_status("Device in init!")
        try:
	    self.Mono = lm.Mono(self.serial_port)
            #self.Monochromator.__init__(self.serial_port)
            self.set_state(PyTango.DevState.ON)
            self.set_status("Device is ON!")
            print("Device is now turned on")
        except Exception:
            print("Error Device could not initialize")
            self.set_state(PyTango.DevState.FAULT)
            self.set_status("Device could not initialize!")

    #def read_shutter(self):
    #    return self.Monochromator.get_shutter()

    #@command
    #def open_shutter(self):
    #    self.Monochromator.open_shutter()
    #@command
    #def close_shutter(self):
    #    self.Monochromator.close_shutter()


    def read_Wavelength(self):
        print('reading')
        print("CHECK: ", self.Mono.get_wavelength())
        return self.Mono.get_wavelength()

    def write_Wavelength(self, wavelength):
        self.Mono.set_wavelength(wavelength)



if __name__ == "__main__":
    Cornerstone.run_server()
