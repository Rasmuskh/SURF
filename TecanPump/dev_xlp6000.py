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

    plunger_acceleration = attribute(label="Slope code",
                                     display_level=DispLevel.OPERATOR,
                                     unit = "2500pulses/s^2",
                                     min_value =0,
                                     max_value =7,
                                     dtype = int,
                                     access = AttrWriteType.READ_WRITE,
                                     doc = "The slope code represents an acceleration.")
    microstepmode = attribute(label="Microstemode status",
                              display_level=DispLevel.OPERATOR,
                              dtype = int,
                              min_value=0,
                              max_value=2,
                              access = AttrWriteType.READ_WRITE,
                              doc = "Toggle microstep mode on and off.")
    number_of_backlash_increments = attribute(label="Backlash",
                                              display_level=DispLevel.OPERATOR,
                                              unit = "",
                                              min_value =0,
                                              max_value =248,
                                              dtype = int,
                                              access = AttrWriteType.READ_WRITE,
                                              doc = "In fine positioning mode max is 248. in normal mode max is 31")


        

    def init_device(self):
        Device.init_device(self)
        self.set_state(PyTango.DevState.INIT)
        self.set_status("Device in init!")
        try:
            self.pump = lib_xlp6000.Pump(serial_port=self.serial_port)
            self.pump.move_valve_to_input_port()
            self.pump.microstepmode=0
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
        return int(self.pump.get_actual_plunger_position())
        #p = float(self.pump.get_actual_plunger_position())
        #p = int(6*float(p-1475))
        return p
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
    def read_plunger_acceleration(self):
        return int(self.pump.get_slope_code_setting())
    def read_microstepmode(self):
        return int(self.pump.get_current_mode())
    def read_number_of_backlash_increments(self):
        return int(self.pump.get_number_of_backlash_increments())

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
    def write_plunger_acceleration(self, n):
        self.pump.set_slope(n)
    def write_microstepmode(self,n):
        self.pump.microstepmode(n)
    def write_number_of_backlash_increments(self, n):
        self.pump.backlash_increments(n)

    @command
    def terminate(self):
        self.pump.terminate_current_command()
    @command
    def simulated_plunger_initialization(self):
        self.pump.simulated_plunger_initialization()





if __name__ == "__main__":
    xlp6000.run_server()
        
