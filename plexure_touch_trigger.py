# code for the capactive touch Pi Hat.
#
# Adapted to trigger Plexure's workflow engine
# 
# when an input is touched or released, call web REST API on Plexure Azure server
#
# Usage: sudo python plexure_touch_trigger.py
#
# Author: Bob
#
import sys
import time
import requests
import socket

import Adafruit_MPR121.MPR121 as MPR121

#
# Parse commandline arguments for URL to send REST POST request to

# if len(sys.argv) < 2:
#    print('Error - missing command line argument - URL to POST updates to')
#    sys.exit(1)

eventType = 'touch'
url = 'https://workflow-events-ingest.azurewebsites.net/api/ingest/'+eventType

print('\n\n=====================================================================')
print('Adafruit MPR121 Capacitive Touch Sensor Test')
print('posting activities to REST API at URL '+ url)

# Create MPR121 instance.
cap = MPR121.MPR121()

# Initialize communication with MPR121 using default I2C bus of device, and
# default I2C address (0x5A).  On BeagleBone Black will default to I2C bus 0.
if not cap.begin():
    print('Error initializing MPR121.  Check your wiring!')
    sys.exit(1)

# Alternatively, specify a custom I2C address such as 0x5B (ADDR tied to 3.3V),
# 0x5C (ADDR tied to SDA), or 0x5D (ADDR tied to SCL).
#cap.begin(address=0x5B)

# Also you can specify an optional I2C bus with the bus keyword parameter.
#cap.begin(busnum=1)

# Init connection to webserver - request most recent activity from Db
# this will also record the device's IP address in the Db
# on booting, pause for 5 seconds while network is initialized
time.sleep(5)

# upload the local LAN IP address (192.168.1.XXX) of the RPi to my webserver so I can then log into it over WiFi  
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('google.com', 0))
localIp = s.getsockname()[0]
s.close()

print('my IP address on local LAN is '+localIp)
r = requests.post(url+'/ip?address='+localIp)
print(r.status_code)

# send a GET to API on startup as a test
r = requests.get(url+'/activity')
print(r.status_code)
print(r.content)

# Main loop to print a message every time a pin is touched.
print('Press Ctrl-C to quit.')
last_touched = cap.touched()

while True:
    current_touched = cap.touched()
    # Check each pin's last and current state to see if it was pressed or released.
    for i in range(12):
        # Each pin is represented by a bit in the touched value.  A value of 1
        # means the pin is being touched, and 0 means it is not being touched.
        pin_bit = 1 << i
        # First check if transitioned from not touched to touched.
        if current_touched & pin_bit and not last_touched & pin_bit:
            print('{0} touched!'.format(i))
            r = requests.post(url+'/activity?activity=touched&code='+str(i))
            print(r.status_code)
            print(r.content)

        # Next check if transitioned from touched to not touched.
        if not current_touched & pin_bit and last_touched & pin_bit:
            print('{0} released!'.format(i))
            r = requests.post(url+'/activity?activity=released&code='+str(i))
            print r.status_code
            print r.content

    # Update last state and wait a short period before repeating.
    last_touched = current_touched
    time.sleep(0.1)

    # Alternatively, if you only care about checking one or a few pins you can
    # call the is_touched method with a pin number to directly check that pin.
    # This will be a little slower than the above code for checking a lot of pins.
    #if cap.is_touched(0):
    #    print('Pin 0 is being touched!')

    # If you're curious or want to see debug info for each pin, uncomment the
    # following lines:
    #print '\t\t\t\t\t\t\t\t\t\t\t\t\t 0x{0:0X}'.format(cap.touched())
    #filtered = [cap.filtered_data(i) for i in range(12)]
    #print('Filt:', '\t'.join(map(str, filtered)))
    #base = [cap.baseline_data(i) for i in range(12)]
    #print('Base:', '\t'.join(map(str, base)))
