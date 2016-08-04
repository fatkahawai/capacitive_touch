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
from datetime import datetime

#import Adafruit_MPR121.MPR121 as MPR121

eventType = 'touch'
url = 'https://workflow-events-ingest.azurewebsites.net/api/ingest/'+eventType
print('posting activities to REST API at URL '+ url)

r = requests.post(url, json = {"pin":61,"action":"touchedTEST"})
print(r.status_code)
print(r.content)

r = requests.post(url, json = {"pin":61,"action":"releasedTEST"})
print(r.status_code)
print(r.content)
