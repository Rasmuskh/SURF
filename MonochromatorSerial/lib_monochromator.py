import serial
import time



class Mono:
    #Constructor
    def __init__(self, serial_port='/dev/ttyUSB0'):
        self.ser = serial.Serial(port=serial_port,
                                 baudrate=9600,
                                 bytesize=8,
                                 stopbits=1,
                                 timeout=2,
                                 parity=serial.PARITY_NONE)
        self.ser.write("HANDSHAKE 0\n")
        self.ser.readlines()
        self.error_checker()


    def read_buffer(self):
        return self.ser.readline()

    #dealing with errors
    #get error messages
    def get_error_msg(self):
        self.ser.write("ERROR?\n")
        response = self.ser.readlines()
        print(response)
        echo, errorcode_string = response
        errorcode = int(errorcode_string[0:1])
        if errorcode ==1:
            error_msg = "Command not understood."
        elif errorcode == 2:
            error_msg = "Bad parameter used in Command."
        elif errorcode == 3:
            error_msg = "Destination position for wavelength motion not allowed."
        elif errorcode == 6:
            errormsg = "Accessory not present (usually filter wheel)."
        elif errorcode == 7:
            errormsg = "Accessory already in specified position."
        elif errorcode == 8:
            errormsg = "Could not home wavelength drive."
        elif errorcode == 9:
            errormsg = "Label too long."
        elif errorcode == 0:
            errormsg = "System error (miscellaneous)."
        else:
            error_msg = "Unknown error code: %s" %errorcode
        return error_msg
    #Get status byte
    def get_STB(self):
        self.ser.write("STB?\n")
        response = self.ser.readlines()
        #print(response)
        echo, STB_string = response
        STB = int(STB_string[0:1])
        return STB
    #check for errors
    def error_checker(self):
        STB = self.get_STB()
        #print('status byte = %d' %STB)
        if STB == 0:
            print("Status byte reports no error!")
        else:
            error_msg=self.get_error_msg()
            print(error_msg)

    #get and set wavelength
    def set_wavelength(self, wavelength):
        self.ser.write("GOWAVE %d\n" %wavelength)
        print('set wavelength response', self.ser.readlines())
        self.error_checker()
    def get_wavelength(self):
        self.ser.write("WAVE?\n")
        response = self.ser.readlines()
        echo, wavelength = response
        wavelength = float(wavelength[0:7])
        self.error_checker()
        return int(wavelength)

    #stop any wavelength adjustment immediately
    def abort(self):
        self.ser.write('ABORT\n')
        print(self.ser.readlines())
        self.error_checker()

    #change the wavelength by some steps between -9999 and 9999
    def set_step(self, n):
        self.ser.write("STEP %d\n" %n)
        print(self.ser.readlines())
        self.error_checker()
    def get_step(self):
        self.ser.write("STEP?\n")
        response = self.ser.readlines()
        echo, step = response
        step = int(step[0:4])
        self.error_checker()
        return step

    #shutter control
    def close_shutter(self):
        self.ser.write("SHUTTER C\n")
        print(self.ser.readlines())
        self.error_checker()
    def open_shutter(self):
        self.ser.write("SHUTTER O\n")
        print(self.ser.readlines())
        self.error_checker()
    def get_shutter(self):
        self.ser.write("SHUTTER?\n")
        response = self.ser.readlines()
        echo, shutter = response
        shutter = shutter[0]
        self.error_checker()
        if shutter == 'O':
            return 'Shutter is open'
        elif shutter == 'C':
            return 'shutter is closed'

    #Switch between grating number one and two
    def set_grating(self, grating_number):
        self.ser.write("GRAT %d\n" %grating_number)
        time.sleep(12)
        print(self.ser.readlines())
        self.error_checker()
    def get_grating(self):
        self.ser.write("GRAT?\n")
        response = self.ser.readlines()
        echo, grating_number = response
        grating_number = int(grating_number[0])
        self.error_checker()
        return grating_number


