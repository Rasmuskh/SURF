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
    serial_port = device_property(dtype = str, default_value= "HR4C5720")

    #attributes



    def init_device(self):
        Device.init_device(self)
        self.set_state(PyTango.DevState.INIT)
        self.set_status("Device in init!")
        try
