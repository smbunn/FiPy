from network import LoRa
import socket
import binascii
import struct
import time   # import library for delay times
import pycom   # library for PyCom stuff like LEDs and IO
import config

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)

# Colors
off = 0x000000
red = 0xff0000
green = 0x00ff00
blue = 0x0000ff
yellow = 0xffff00
# Set up KotahiNet channels
lora.add_channel(0, frequency=864862500, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=865062500, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=865402500, dr_min=0, dr_max=5)
lora.add_channel(3, frequency=865602500, dr_min=0, dr_max=5)
lora.add_channel(4, frequency=865985000, dr_min=0, dr_max=5)
lora.add_channel(5, frequency=866200000, dr_min=0, dr_max=5)
lora.add_channel(6, frequency=866400000, dr_min=0, dr_max=5)
lora.add_channel(7, frequency=866600000, dr_min=0, dr_max=5)

# Turn off hearbeat LED
pycom.heartbeat(False)

# create an ABP authentication params
dev_addr = struct.unpack(">l", binascii.unhexlify('00 70 C3 4D'.replace(' ','')))[0]
nwk_swkey = binascii.unhexlify('1BFE9C81AD35B39019244D155CE31D88'.replace(' ',''))
app_swkey = binascii.unhexlify('045ABBEFE974D3E257AC31522E8E837B'.replace(' ',''))

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)

# make the socket blocking
s.setblocking(True)

# send some data
for count in range (20):  #Run this loop for 200 times. Possibly it would be better to run infinite.
# make the socket blocking
    s.setblocking(True)
    pycom.rgbled(off)   # flash the LED
    time.sleep(0.6)
    pycom.rgbled(red)
    time.sleep(2)
    pycom.rgbled(off)
    buffer = b'test123 ' + bytes([count])  # Build what we want to send in the Send buffer
    #the test123 is static and the bytes count will progress to tell us that different data is being sent
    print('Send number', count, 'Buffer=', buffer) # Print Buffer for debugging
    s.send(buffer)  # send buffer to TTN

    #s.send(bytes([0x01, 0x02, 0x03, 0x04]))
    print('data sent')

# get any data received&
    s.setblocking(False)
    data = s.recv(64)
    print(data)
    time.sleep(58)  # wait time between join tries
