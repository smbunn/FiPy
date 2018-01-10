from network import LoRa  #import information library for Lora
import socket   # setup a socket library for sending and receiving
import time   # import library for delay times
import pycom   # library for PyCom stuff like LEDs and IO
import config
import binascii

  # Turn off hearbeat LED
pycom.heartbeat(False)

   # create a lora object that is used in the program
lora = LoRa(mode=LoRa.LORAWAN, public=True, adr=False)

  #Setting up channels for sub-band 2 for TTN  (US Only)  Europe may be different
# set the 3 default channels to the same frequency (must be before sending the OTAA join request)
lora.add_channel(0, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)

# create an OTA authentication params
dev_eui = binascii.unhexlify('70 B3 D5 49 97 69 FC BD'.replace(' ','')) # these settings can be found from TTN
app_eui = binascii.unhexlify('70 B3 D5 7E F0 00 44 5B'.replace(' ','')) # these settings can be found from TTN
app_key = binascii.unhexlify('C5E7B6E6A6C413A2E959A3194193BA2E'.replace(' ','')) # these settings can be found from TTN

# for index in range(0, 8):  #turn off channels 0-7
#      lora.remove_channel(index)

# 3for index in range(16, 65): #turn off channels 16-64
#     lora.remove_channel(index)

# for index in range(66, 72): #turn off channels 66-71
#     lora.remove_channel(index)

  # setup Activation App EUI first cut and past from TTN, (msb) App Key cut and paste (msb). Format is as below.
  # Hit the <> before hit the copy button to get this format . You may need to put in the commas

print("Starting Join...")  # debug to tell user we are starting the join
lora.join(activation=LoRa.ABP, auth=(dev_eui, app_eui, app_key), timeout=0)  # setup OTAA and authentication
  # Timeout needs to be 0 for US.  haven't experimented with other values

x=0  # setup a counter for how many times it takes to join
  # Loop and wait until the module has joined the network
while (not lora.has_joined() and x<10):
     time.sleep(2.5)  # wait time between join tries
     print('Lora Joining...');
     x=x+1
     print('Lora has joined?= ', lora.has_joined())
     #print(lora.)   /  Print lora connect parameters
     # could quit program here if it didn't join in x number of tries

         # Joining looks like this on Debug screen:
     # Starting Join...
     # Lora Joining...
     # Lora has joined?=  False
     # Lora Joining...
     # Lora has joined?=  False
     # Lora Joining...
     # Lora has joined?=  True
  # Joined Lora TTN OTAA. Now creates a socket for Lora send and receive
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)  # setup socket for raw transmission
  #used for string sends
  # set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)  #setup socket for US data rate
 #s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)  # for Europe  (May need othe rchanges for Euorpe)

# lora.remove_channel(65); #drop the 500khz channel
 # not sure why this is needed or if it is needed

  # make the socket non-blocking
s.setblocking(False)  #Set non-blocking so we don't get stuck if no receive data is available
time.sleep(5.0)  #wait a little bit after a join to send the first data

if (lora.has_joined()):  # check to see if joined TTN in OTAA configuration
     print('Joined...')  # tell debug that we joined

     for count in range (200):  #Run this loop for 200 times. Possibly it would be better to run infinite.
 # while(1)   # use this line and comment out about to run infinite
 # count = count +1   # use count if using while(1) so our count can increase
  # Send Section
         buffer = b'test123 ' + bytes([count])  # Build what we want to send in the Send buffer
         #the test123 is static and the bytes count will progress to tell us that different data is being sent
         print('Send number', count, 'Buffer=', buffer) # Print Buffer for debugging
         s.send(buffer)  # send buffer to TTN

         #Sent data looks like this on Debug screen:
     # Send number 0 Buffer= b'test123 \x00'
     # Send number 1 Buffer= b'test123 \x01'
     # Send number 2 Buffer= b'test123 \x02'
     # Send number 3 Buffer= b'test123 \x03'
  # Receive section
  # For testing go to TTN Device and enter  32 01 34 in the downlink - The Blue light will come on
  # Received data will look like this on Debug screen - Received Data = b'2\x014'
  # For testing go to TTN Device and enter  35 00 36 in the downlink - The Blue light will come on
  # Received data will look like this on Debug screen - Received Data = b'5\x006'
  # Receive happens 1 second after each send - Receive window opens
         #time.sleep(1)  # sleep between send and receive.  Haven't found it necessary and can cause problems if too large
         rx = s.recv(10)  #Receive up to 10 bytes  possibly can take more - Won't wait for receive data
         if rx:  # Check for received data from TTN
             print('Received Data =', rx, 'Byte1=', rx[1] )  # Print received data for debugging
             if (len(rx) >2):  # if receive has 2 or more bytes check for 01 value
             # if not just sleep
                 print("Length of rx=", len(rx))  #debug length of received data
                 if rx[1] == 1:   # if byte 1 (second byte) is value 1
                     print('Receive Found 01 - LED Blue')  # if found 01 in second byte print that it is found
                     pycom.rgbled(0x00007f) # Set light to Blue
                 else:
                     print('Receive did not Find 01 - LED Red')  # if not found 01 in second byte print that it is not found
                     pycom.rgbled(0x7f0000) # Set light to red

         time.sleep(10)   # sleep here so we don't transmit too much suggest 10  for test and 120 or more for regular operation.
    #pycom.rgbled(0x000000) # Turn light off after sleeping if desired.
pycom.rgbled(0x7f7f00) # Set light to yellow - All 200 transmissions have completed.
