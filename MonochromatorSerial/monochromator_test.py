"""Send Statements = Queries and commands. Receive Responses"""

import serial

ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, bytesize=8, stopbits=1, timeout=3, parity=serial.PARITY_NONE)

print("port: ",ser.name)

ser.write("HANDSHAKE 1\n")
print("getting response")
print(ser.readline()) #echo
print(ser.readline()) #error code

ser.write("WAVE?\n")
print("getting response")
print(ser.readline()) #echo
print(ser.readline()) #answer
print(ser.readline()) #error code

ser.write("GOWAVE 500\n")
print("getting response")
print(ser.readline()) #echo
print(ser.readline()) #error code
#ser.write("{ERROR?}\n")
ser.write("STB?\n")
print("getting status bit")
print(ser.readline()) #echo
print(ser.readline()) #answer
print(ser.readline()) #error code
