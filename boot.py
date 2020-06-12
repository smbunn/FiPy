# boot.py -- run on boot-up
import machine
from network import WLAN
wlan = WLAN() # get current object, without changing the mode

if machine.reset_cause() != machine.SOFT_RESET:
    wlan.init(mode=WLAN.STA, antenna = WLAN.EXT_ANT)
    # configuration below MUST match your home router settings!!
    wlan.ifconfig(config=('192.168.1.252', '255.255.255.0', '192.168.1.2', '192.168.1.2'))

if not wlan.isconnected():
    # change the line below to match your network ssid, security and password
    wlan.connect(ssid='TheBunns', auth=(WLAN.WPA2, 'nowisthetime'), timeout=5000)
    while not wlan.isconnected():
        machine.idle() # save power while waiting
# update gateway
