import pycom
import time
pycom.heartbeat(False)
for cycles in range(10): # stop after 10 cycles
    pycom.rgbled(0x007f00) # green
    time.sleep(2)
    pycom.rgbled(0x00007f) # blue
    time.sleep(2)
    pycom.rgbled(0x7f0000) # red
    time.sleep(2)