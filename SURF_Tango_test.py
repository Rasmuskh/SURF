import tango

#initialize Monochromator
M = tango.DeviceProxy('test/Cornerstone/1')
M.set_timeout_millis(30000)
#Initialize pump
P = tango.DeviceProxy('test/XLP6000/1')
P.set_timeout_millis(30000)
#initialize Spectrometers
UV = tango.DeviceProxy('test/HR4000/1')
FL = tango.DeviceProxy('test/QE65000/1')


