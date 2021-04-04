# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 09:00:22 2021

@author: Vijeeth Rakshakar
"""
import serial
import struct
import time

ser = serial.Serial()
ser.baudrate = 115200
ser.port = '/dev/ttyUSB0'
ser.timeout = 1
ser.open()
time.sleep(0.5)
ser.reset_input_buffer()
ser.reset_output_buffer()

ser.write('./scanftest\n'.encode())
data = ser.readline()
print(data)
time.sleep(1)

ser.write(b'Width: 20\n')
ser.write(b'Height: 20\n')

print(ser.inWaiting())
print(ser.timeout)


data = ser.readline() # b'Width: 4\n'
print(data)
data = ser.readline() # b'Height: 3\n'
print(data)
data = ser.readline() # Actual OUTPUT
print(data)

for i in range(400):
    ser.write(str(i).encode() + b'\n')
    ser.readline()
    data = ser.readline() # Actual OUTPUT
    print(data)

data = ser.readline() # Actual OUTPUT
print(data)



ser.close()
