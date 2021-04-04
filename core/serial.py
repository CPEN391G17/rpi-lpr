# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 09:00:22 2021

@author: Vijeeth Rakshakar
"""
import serial
import struct
import time
from PIL import Image
import numpy as np
import pysftp
from PIL import Image
import scipy.misc

def grayscale_and_resize(image):
    print(type(image))
    ethernet = '169.254.10.9'
    serial_port = '/dev/ttyUSB0'

    #im = Image.open('car2.jpg','r')
    im = Image.fromarray(image)
    pix_val = list(im.getdata())
    pix_val_flat = [x for sets in pix_val for x in sets+(4,)]
    file = open("input.bin", "wb")
    file.write(bytes(pix_val_flat))
    file.close()

    # Accept any host key
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    # And authenticate with a private key
    sftp = pysftp.Connection(host=ethernet, username='root', password='terasic', private_key=".ppk", cnopts=cnopts)
    with sftp.cd('/home/root'):             # temporarily chdir to public
            sftp.put('input.bin')  # upload file to public/ on remote

    width, height = im.size

    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = serial_port
    ser.timeout = 1
    ser.open()

    while ser.inWaiting() > 0:
        ser.readline()

    print("Waiting",ser.inWaiting())

    ser.write('./load_resize_linux_test\n'.encode())
    data = ser.readline()
    print(data)
    time.sleep(1)

    ser.write(b'Width: '+str(width).encode()+b'\n')
    ser.write(b'Height: '+str(height).encode()+b'\n')

    print(ser.inWaiting())
    print(ser.timeout)


    data = ser.readline() # b'Width: 4\n'
    print(type(data))
    print(data)
    data = ser.readline() # b'Height: 3\n'
    print(data)

    output_pixels = []
    new_width = 3*(width-1)
    new_height = 3*(height-1)

    data = ser.readline()
    while data != b'done\r\n':
        print(data)
        data = ser.readline()

    # for i in range(new_width*new_height):
    #     data =ser.readline()
    #     output_pixels.append(int(data.decode()[:2], 16))
    #     if i % 50 == 0:
    #         print(i)

    # B = np.reshape(output_pixels, (new_width, new_height))

    # img = Image.fromarray(B)
    # img.show()

    # data = ser.readline() # Actual OUTPUT
    # print(data)
    # print(data == b'done\r\n')
    # data = ser.readline() # Actual OUTPUT
    # print(data)
    # print(data == b'done\r\n')
    # data = ser.readline() # Actual OUTPUT
    # print(data)
    # print(data == b'done\r\n')


    # Accept any host key
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    # And authenticate with a private key
    sftp = pysftp.Connection(host=ethernet, username='root', password='terasic', private_key=".ppk", cnopts=cnopts)
    with sftp.cd('/home/root'):             # temporarily chdir to public
    	sftp.get('output.bin')  # upload file to public/ on remote

    file = open("output.bin", "rb")

    output_list = []
    byte = file.read(4)
    while byte:
        output_list.append(int.from_bytes(byte, "little"))
        byte = file.read(4)

    print(len(output_list))


    B = np.reshape(output_list, ((height - 1)*3, (width - 1)*3))

    print(B)
    #rgb = scipy.misc.toimage(B)

    #img = Image.fromarray(B)
    #img.show()
    #img.save('img.png')

    ser.close()

    return B.astype('uint8')
