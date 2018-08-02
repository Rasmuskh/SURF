import serial as sr 
comm = sr.Serial(port = '/dev/ttyUSB0', baudrate = 9600, bytesize = sr.EIGHTBITS, parity = sr.PARITY_NONE, stopbits = sr.STOPBITS_ONE, timeout = 2)#dummy usb address. may differ.

cmd='02h31h00110001?403h'

comm.write(cmd)#.encode('utf-8'))

comm.read(2)


