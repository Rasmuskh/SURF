import numpy
import PyTango
from PyTango import DispLevel, AttrWriteType, DevState
from PyTango.server import DeviceMeta, Device, server_run
from PyTango.server import command, attribute, device_property

import lib_monochromator as lm

class Cornerstone(Device):
    __metaclass__ = DeviceMeta
    #properties
    serial_port = device_property(dtype = str, default_value= "/dev/ttyUSB1")

    #attributes
    wavelength = attribute(label = "Wavelength", unit ="nm",
                           display_level=DispLevel.OPERATOR,
                           min_value = 0, max_value = 1600,
                           dtype = int, access = AttrWriteType.READ_WRITE,
                           doc = "Choose the wavelength the monochromator lets through.")

    step = attribute(label = "step",
                     display_level=DispLevel.OPERATOR,
                     min_value=-9999, max_value=9999,
                     dtype = int, access = AttrWriteType.READ_WRITE,
                     doc = "number of steps to increase wavelength (unit is not nm).")
    grating = attribute(label = "grating number",
                        display_level=DispLevel.OPERATOR,
                        min_value = 1, max_value = 2,
                        dtype = int, access = AttrWriteType.READ_WRITE,
                        doc = "Choose wether to use grating one or grating two.")

    shutter = attribute(label = "Shutter status",
                        display_level=DispLevel.OPERATOR,
                        min_value = 0, max_value = 1,
                        dtype = int, access = AttrWriteType.READ_WRITE,
                        doc = "Shutter can be either open=1 or closed=0.")


    def init_device(self):
        Device.init_device(self)
        self.set_state(PyTango.DevState.INIT)
        self.set_status("Device in init!")
        try:
            self.Mono = lm.Mono(serial_port=self.serial_port)
            self.set_state(PyTango.DevState.ON)
            self.set_status("Device is ON!")
            print("Device is now turned on")
        except Exception:
            print("Error Device could not initialize")
            self.set_state(PyTango.DevState.FAULT)
            self.set_status("Device could not initialize!")

    #@command
    #def close_serialport(self):
    #    self.Mono.close_serialport()
    #    self.set_state(PyTango.DevState.OFF)
    #    self.set_status("Connection stopped. press init to reestablish.")

    def read_shutter(self):
        return self.Mono.get_shutter()

    def write_shutter(self, n):
        if n == 0:
            self.Mono.close_shutter()
        elif n == 1:
            self.Mono.open_shutter()
        else:
            raise ValueError
    # def open_shutter(self):
    #     self.Mono.open_shutter()
    # def close_shutter(self):
    #     self.Mono.close_shutter()


    def read_wavelength(self):
        return self.Mono.get_wavelength()
    def write_wavelength(self, wavelength):
        self.Mono.set_wavelength(wavelength)

    def read_grating(self):
        return self.Mono.get_grating()
    def write_grating(self, n):
        self.Mono.set_grating(n)

    def read_step(self):
        return self.Mono.get_step()
    def write_step(self, steps):
        self.Mono.set_step(steps)



if __name__ == "__main__":
    Cornerstone.run_server()
