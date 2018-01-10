from network import LoRa
import socket
import binascii
import struct
import config


# Initialize LoRa in LORAWAN mode.

lora = LoRa(mode=LoRa.LORAWAN)

# set the 3 default channels to the same frequency (must be before sending the OTAA join request)
lora.add_channel(0, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)

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
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

# send some data
s.send(bytes([0x01, 0x02, 0x03]))

# make the socket non-blocking
# (because if there's no data received it will block forever...)
s.setblocking(False)

# get any data received (if any...)
data = s.recv(64)
print(data)
