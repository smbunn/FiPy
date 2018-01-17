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

# Colors
off = 0x000000
red = 0xff0000
green = 0x00ff00
blue = 0x0000ff
yellow = 0xffff00

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)

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

for count in range (2000):
    py = Pysense()
    mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
    si = SI7006A20(py)
    lt = LTR329ALS01(py)
    li = LIS2HH12(py)
    print("Count=", count)
    print("MPL3115A2 temperature: " + str(mp.temperature()))
    print("Altitude: " + str(mp.altitude()))
    mpp = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
    print("Pressure: " + str(mpp.pressure())) #Pressure does not work too well
    print("Temperature: " + str(si.temperature())+ " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")
    print("Dew point: "+ str(si.dew_point()) + " deg C")
    t_ambient = 24.4
    print("Humidity Ambient for " + str(t_ambient) + " deg C is " + str(si.humid_ambient(t_ambient)) + "%RH")
    print("Light (channel Blue lux, channel Red lux): " + str(lt.light()))
    print("Acceleration: " + str(li.acceleration()))
    print("Roll: " + str(li.roll()))
    print("Pitch: " + str(li.pitch()))
    vt = py.read_battery_voltage()
    print("Battery voltage: " + str(py.read_battery_voltage()))
    pycom.rgbled(blue)
    time.sleep(0.5)
    pycom.rgbled(off)
    time.sleep(0.5)
    pycom.rgbled(red)
    time.sleep(0.5)
    pycom.rgbled(off)
    s.setblocking(True)
    data = bytearray(2)
    data = bytearray(struct.pack(">f", vt))
    s.send(data)  # send buffer to TTN

    #s.send(bytes([0x01, 0x02, 0x03, 0x04]))
    print('data sent')
    time.sleep(0.5)
    # get any data received&
    s.setblocking(False)
    data = s.recv(64)
    time.sleep(0.5)
    print(data)  #anything received?time.sleep(20)  # wait time between packets sent
    time.sleep(58)
