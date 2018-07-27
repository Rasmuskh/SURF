#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
#                                                 #
#          Script for speaking with pump          #
#                                                 #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
import sys
import serial as sr

#Establish communication line
comm = sr.Serial('/dev/ttyUSB0')#dummy usb address. may differ.
#Choose an adress for the pump. 0<=>'31h', 1<=>'32h', 15<=>'3Eh', self-test<=>'3Fh'
#Address '30h' is the address of the computer
addr = '31h'



# Implement a response parser.
# all commands should be preceeded by Q command to check pump status
# and check for errors
# the response will contain error code: bit0-3 and status bit5. what about 4? or is 0 the first and so 3 is the fourth and four is the fifth?




#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#       Configuration commands        #
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
def setMicroStepMode(n):
    """[N<n>] Set Microstep Mode Off/On. Manual ch3 p21
    <n> = 0(normal mode), 1(fine pos mode) or 2(micro-step mode). """
    comm.write(+addr+'N'+n++'R')#This command is not run untill an R has been received
    res = comm.read()
    return res
def setBacklashIncrements(n):
    """[K<n>] Backlash Increments. Manual ch3 p22
    where <n> = 0..31 in full step mode (12 is the default),
    and <n> = 0..248 in fine positioning mode (96 is the default)."""
    comm.write(+addr+'K'+n++'R')#This command is not run untill an R has been received
    res = comm.read()
    return res
def setPumpConfig(n):
    """[U<n>] Write Pump Configuration to Non-Volatile Memory."""
    comm.write(+addr+'U'+n++'R')#This command is not run untill an R has been received
    res = comm.read()
    return res

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#       initialization commands       #
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
def setSyringeDeadVolume(n):
    """[k<n>] Choose syringe dead volume. Manual ch3 p24.
    <n> = the offset in increments from top of travel
    <n> = 0..255 (122 is the default)
    <n> = 0..2040 in fine positioning and microstep modes (976 is the default)"""
    n='122'
    comm.write(+addr+'k'+n++'R')#This command is not run untill an R has been received
    res = comm.read()
    return res
def initPlungerAndValveDriveCW(n1, n2, n3):
    """[Z<n1,n2,n3>] Initialize Plunger and Valve Drive. Clockwise polarity. Manual ch3 p25.
    n1 = Set initialization plunger force/speed
    n2 = Set initialization input port
    n3 = Set initialization output port"""
    comm.write(+addr+'Z'+n1+','+n2+','+n3)
    res = comm.read()
    return res
def initPlungerAndValveDriveCCW(n1, n2, n3):
    """[Y<n1,n2,n3>] Initialize Plunger and Valve Drive. Counterclockwise polarity. Manual ch3 p25.
    n1 = Set initialization plunger force/speed
    n2 = Set initialization input port
    n3 = Set initialization output port"""
    comm.write(+addr+'Y'+n1+','+n2+','+n3)
    res = comm.read()
    return res
def initPlungerDrive(n):
    """[W<n>] This command initializes the plunger drive only (commonly used for valveless pumps)."""
    comm.write(+addr+'W'+n)
    res = comm.read()
    return res
def initValveDrive(n1, n2):
    """[w<n1,n2>] This command initializes the valve drive only."""
    comm.write(+addr+'w'+n1+n2)
    res = comm.read()
    return res
def simulatedPlungerInitialization():
    """The [z] command simulates an initialization of the plunger drive, however, 
    no mechanical initialization occurs. The current position of the plunger is
    set as the zero (home) position."""
    comm.write(+addr+'z')
    res = comm.read()
    return res

#W 
#w
#z








#close port
comm.close()
