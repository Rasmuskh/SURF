import numpy
import PyTango
from PyTango import DispLevel, AttrWriteType, DevState
from PyTango.server import DeviceMeta, Device, server_run
from PyTango.server import command, attribute, device_property

import lib_xlp6000

class xlp6000(Device):
    """XLP6000 pump class"""

    __metaclass__ = DeviceMeta
    #properties
    serial_port = device_property(dtype = str, default_value= "/dev/ttyUSB0")

    #attributes
    top_speed = attribute(label="Top speed",
                          display_level=DispLevel.OPERATOR,
                          unit = "pulses/s",
                          min_value =5,
                          max_value =6000,
                          dtype = int,
                          access = AttrWriteType.READ_WRITE)

    cutoff_speed = attribute(label="Cutoff speed",
                             display_level=DispLevel.OPERATOR,
                             unit = "pulses/s",
                             min_value =50,
                             max_value =2700,
                             dtype = int,
                             access = AttrWriteType.READ_WRITE,
                             doc = "In normal mode max is 750, in microstep max is 2700. min is always 50.")

    start_speed = attribute(label="Start speed",
                             display_level=DispLevel.OPERATOR,
                             unit = "pulses/s",
                             min_value =50,
                             max_value =1000,
                             dtype = int,
                             access = AttrWriteType.READ_WRITE)

    plunger_position = attribute(label="Position",
                                 display_level=DispLevel.OPERATOR,
                                 unit = "half increments or microsteps",
                                 min_value =0,
                                 max_value =48000,
                                 dtype = int,
                                 access = AttrWriteType.READ_WRITE,
                                 doc="Units are given in half increments or microsteps for nomral mode and microstep mode respectively. max value in normal mode is 6000 and in microstep mode it is 48000")

    valve_position = attribute(label="Valve position",
                               display_level=DispLevel.OPERATOR,
                               unit = "",
                               min_value =0,
                               max_value =2,
                               dtype = int,
                               access = AttrWriteType.READ_WRITE,
                               doc="The valve has three positions: 0=input, 1=output, 2=bypass.")

    device_status = attribute(label="Device status",
                               display_level=DispLevel.EXPERT,
                               dtype = str,
                               access = AttrWriteType.READ,
                               doc="Device status/error codes. See pump manual for explanation of codes.")
    voltage = attribute(label="Voltage",
                        display_level=DispLevel.EXPERT,
                        unit = "V",
                        dtype = float,
                        access = AttrWriteType.READ,
                        doc="The voltage supplied to the pump.")


        

    def init_device(self):
        Device.init_device(self)
        self.set_state(PyTango.DevState.INIT)
        self.set_status("Device in init!")
        try:
            self.pump = lib_xlp6000.Pump(self.serial_port)
            self.pump = lib_xlp6000.Pump()
            self.set_state(PyTango.DevState.ON)
            self.set_status("Device is ON!")
            print("Device is now turned on")
        except Exception:
            print("Error Device could not initialize")
            self.set_state(PyTango.DevState.FAULT)
            self.set_status("Device could not initialize!")

    #read commands
    def read_top_speed(self):
        return int(self.pump.get_top_speed())
    def read_cutoff_speed(self):
        return int(self.pump.get_cutoff_speed())
    def read_start_speed(self):
        return int(self.pump.get_start_speed())
    def read_plunger_position(self):
        #return int(self.pump.get_absolute_plunger_position())
        return int(self.pump.get_actual_plunger_position())
    def read_valve_position(self):
        response = self.pump.get_valve_position()
        if response == "i":
            response = 0
        elif response == "o":
            response = 1
        elif response == "b":
            response =2
        else:
            raise ValueError("valve position passed from pump must be either i, o or b.")
        return response
    def read_device_status(self):
        return self.pump.get_error_code()
    def read_voltage(self):
        return float(self.pump.get_voltage())/10
    #write commands
    def write_top_speed(self, n):
        self.pump.set_top_speed(n)
    def write_cutoff_speed(self, n):
        self.pump.set_cutoff_speed(n)
    def write_start_speed(self, n):
        self.pump.set_start_speed(n)
    def write_plunger_position(self, n):
        self.pump.move_plunger_absolute_position(n)
    def write_valve_position(self, n):
        if n==0:
            self.pump.move_valve_to_input_port()
        elif n==1:
            self.pump.move_valve_to_output_port()
        elif n==2:
            self.pump.move_valve_to_bypass_position()
    
                        






if __name__ == "__main__":
    xlp6000.run_server()
        
