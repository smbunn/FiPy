# See https://docs.pycom.io for more information regarding library specifics
from network import LoRa
#import config
from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
import time   # import library for delay times
import pycom
import socket
import binascii
import struct
import ujson

# Colors
off = 0x000000
red = 0xff0000
green = 0x00ff00
blue = 0x0000ff
yellow = 0xffff00

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN, bandwidth=LoRa.BW_500KHZ, region=LoRa.AU915, public=True)
# leave channels 8-15 and 65
for index in range(0, 8):
   lora.remove_channel(index)  # remove 0-7
for index in range(16, 65):
   lora.remove_channel(index)  # remove 16-64
for index in range(66, 72):
  lora.remove_channel(index)   # remove 66-71
# Turn off hearbeat LED
pycom.heartbeat(False)

# create an ABP authentication params
dev_addr = struct.unpack(">l", binascii.unhexlify('26 00 2C 58'.replace(' ','')))[0]
nwk_swkey = binascii.unhexlify('37 70 5E 6D F5 04 8F 2F 42 87 E5 3F 09 78 A9 11'.replace(' ',''))
app_swkey = binascii.unhexlify('A1 13 D6 0F 1A 9C 08 9F E6 94 D6 83 76 9F 8B DE'.replace(' ',''))

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 6)

# Builds the bytearray to send the request
py = Pysense()
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)
mpp = MPL3115A2(py) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters

for count in range (999999):
    print("Count=", count)
    vt = py.read_battery_voltage()
    print("Battery voltage: " +str(vt))
    dew = si.dew_point()
    print("Dew point: "+ str(dew) + " deg C")
    temp1 = mpp.temperature()
    print("Tempertaure1: " + str(temp1))
    press1 = mpp.pressure()
    print("Pressure: " + str(press1)) #Pressure does not work too well
    temp2 = si.temperature()
    hum1 = si.humidity()
    print("Temperature: " + str(temp2)+ " deg C and Relative Humidity: " + str(hum1) + " %RH")
    t_ambient = 24.4
    relhum = si.humid_ambient(t_ambient)
    print("Humidity Ambient for " + str(t_ambient) + " deg C is " + str(relhum) + "%RH")
    print("Light (channel Blue lux, channel Red lux): " + str(lt.light()))
    acct = li.acceleration()
    acc1 = acct[0]
    acc2 = acct[1]
    acc3 = acct[2]
    roll1 = li.roll()
    pitch1 = li.pitch()
    print("Acceleration: " + str(acc1) + "  " + str(acc2) + "  " + str(acc3))
    print("Roll: " + str(roll1))
    print("Pitch: " + str(pitch1))
    # Flash the light every time a payload is sent
    pycom.rgbled(blue)
    time.sleep(0.5)
    pycom.rgbled(off)
    time.sleep(0.5)
    pycom.rgbled(red)
    time.sleep(0.5)
    pycom.rgbled(off)
    data = bytearray(48)
    data[0:4] = bytearray(struct.pack(">i", count))
    data[4:8] = bytearray(struct.pack(">f", vt))
    data[8:12] = bytearray(struct.pack(">f", dew))
    data[12:16] = bytearray(struct.pack(">f", temp1))
    data[16:20] = bytearray(struct.pack(">f", roll1))
    data[20:24] = bytearray(struct.pack(">f", press1))
    data[24:28] = bytearray(struct.pack(">f", temp2))
    data[28:32] = bytearray(struct.pack(">f", hum1))
    data[32:36] = bytearray(struct.pack(">f", relhum))
    data[36:40] = bytearray(struct.pack(">f", acc1))
    data[40:44] = bytearray(struct.pack(">f", acc2))
    data[44:48] = bytearray(struct.pack(">f", acc3))
#    data[48:52] = bytearray(struct.pack(">f", roll1))
#    data[52:56] = bytearray(struct.pack(">f", pitch1))
    print ('Data = count     vt      dew    temp1   roll1    press1    temp2    hum1    relhum    acc1       acc2        acc3       pitch1')
    print ('Data = ',count,'  ', vt,dew, temp1, roll1, press1, temp2, hum1, relhum, acc1, acc2, acc3, pitch1 )
    s.setblocking(True)
    s.send(data)  # send buffer to AWS
    print('data sent') #print the sent data fields
    time.sleep(0.5)
    # get any data received&
    s.setblocking(False)
    data_in = s.recv(64)
    time.sleep(0.5)
    print('Data received =',data_in)  #anything received?time.sleep(59)
    time.sleep(51) # wait time between packets sent
