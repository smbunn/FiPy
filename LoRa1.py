""" OTAA Node example compatible with the LoPy Nano Gateway """

from network import LoRa
import pycom
import socket
import binascii
import struct
import time
import config

# Colors
off = 0x000000
red = 0xff0000
green = 0x00ff00
blue = 0x0000ff
yellow = 0xffff00

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)
print('Device ID: ' + binascii.hexlify(lora.mac()).lower().decode('utf-8'))

# Turn off hearbeat LED
pycom.heartbeat(False)

# create an OTA authentication params
#dev_eui = binascii.unhexlify('70 B3 D5 49 97 69 FC BD'.replace(' ','')) # these settings can be found from TTN
#app_eui = binascii.unhexlify('70 B3 D5 7E F0 00 44 5B'.replace(' ','')) # these settings can be found from TTN
#app_key = binascii.unhexlify('E3523D4CD9576F3A64410E369C52407B'.replace(' ','')) # these settings can be found from TTN

# create an ABP authentication params
dev_addr = struct.unpack(">l", binascii.unhexlify('26 01 1D 6A'.replace(' ','')))[0]
nwk_swkey = binascii.unhexlify('B1A32A6A4BA0CAF343B5404D2A54AB88'.replace(' ',''))
app_swkey = binascii.unhexlify('4EC93B4F80C82C3861E8AB3C42A5A05A'.replace(' ',''))

# set the 3 default channels to the same frequency (must be before sending the OTAA join request)
lora.add_channel(0, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)

# join a network using OTAA
#lora.join(activation=LoRa.ABP, auth=(dev_eui, app_eui, app_key), timeout=0) #, dr=config.LORA_NODE_DR)
# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

pycom.rgbled(red)

# wait until the module has joined the network
while not lora.has_joined():
    pycom.rgbled(off)
    time.sleep(0.5)
    pycom.rgbled(red)
    time.sleep(2)
    print('Not joined yet...')

print('Joined network...')
pycom.rgbled(blue)

# remove all the non-default channels
for i in range(3, 16):
    lora.remove_channel(i)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# make the socket blocking
s.setblocking(True)

# send some dataCCCCC
for count in range (2000):  #Run this loop for 20 times.
# make the socket blocking
    s.setblocking(True)
    pycom.rgbled(off)   # flash the LED
    time.sleep(0.6)
    pycom.rgbled(red)
    time.sleep(2)
    pycom.rgbled(off)
    buffer = 'test123 ' + str(count)  # Build what we want to send in the Send buffer
    #the test123 is static and the bytes count will progress to tell us that different data is being sent
    print('Send number', count, 'Buffer=', buffer) # Print Buffer for debugging
    s.send(buffer)  # send buffer to TTN

    #s.send(bytes([0x01, 0x02, 0x03, 0x04]))
    print('data sent')
    time.sleep(0.5)
# get any data received&
    s.setblocking(False)
    data = s.recv(64)
    time.sleep(0.5)
    print(data)  #anything received?
    time.sleep(18)  # wait time between packets sent
