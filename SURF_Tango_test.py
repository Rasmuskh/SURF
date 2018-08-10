import tango

#initialize Monochromator
print("-------------------------------------------------")
M = tango.DeviceProxy('test/Cornerstone/1')
M.set_timeout_millis(30000)
print("--------Monochromator Initialized as M-----------")
#Initialize pump
P = tango.DeviceProxy('test/XLP6000/1')
P.set_timeout_millis(30000)
print("--------Pump Initialized as P--------------------")
#initialize Spectrometers
UV = tango.DeviceProxy('test/HR4000/1')
print("--------UV Spectrometer Initialized as UV--------")
FL = tango.DeviceProxy('test/QE65000/1')
print("--------Fl Spectrometer Initialized as FL--------")
print("-------------------------------------------------")
print("--------Command sequence example:----------------")
print("import matplotlib.pyplot as plt")
print("M.wavelength=550")
print("M.shutter = 1")
print("FL.darkcorrection = True")
print("FL.integrationtime=5000")
print("FL.scanstoaverage=5")
print("plt.plot(FL.spectrum);plt.show()")
print("-------------------------------------------------")

