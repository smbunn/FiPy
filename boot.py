# boot.py -- run on boot-up
import machine
from network import WLAN
wlan = WLAN() # get current object, without changing the mode

if machine.reset_cause() != machine.SOFT_RESET:
    wlan.init(mode=WLAN.STA)
    # configuration below MUST match your home router settings!!
    wlan.ifconfig(config=('192.168.110.252', '255.255.255.0', '192.168.110.1', '192.168.110.1'))

if not wlan.isconnected():
    # change the line below to match your network ssid, security and password
    wlan.connect(ssid='Derceto24', auth=(WLAN.WPA2, 'nothingbutnet'), timeout=5000)
    while not wlan.isconnected():
        machine.idle() # save power while waiting
