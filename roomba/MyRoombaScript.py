"""
Based on examples/complicated.py
"""
import asyncio
from roomba import Roomba
import paho.mqtt.client as mqtt
import time
import json
import logging
import sys

#Uncomment the following two lines to see logging output
logging.basicConfig(level=logging.INFO, 
      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#put your own values here
broker = "localhost"    #ip of mqtt broker
#user = 'user'           #mqtt username
#password = 'password'   #mqtt password
user = None           #mqtt username
password = None   #mqtt password
#broker = None if not using local mqtt broker

address = ""
if (len(sys.argv) == 2):
    address = str(sys.argv[1])

#blid = ""
#roombaPassword = ""

loop = asyncio.get_event_loop()

if address == "":
    print("ERROR: address left empty")
    exit(-1)

#myroomba = Roomba(address)  #minimum required to connect on Linux Debian system, will read connection from config file
#myroomba = Roomba(address, blid, roombaPassword)  #setting things manually
# The web interface is now available in a web browser at http://localhost:8200/map/map.html
myroomba = Roomba(address, webport=8200)

#all these are optional, if you don't include them, the defaults will work just fine
#if you are using maps:
"""
- mapSize is required, and is of the form: '(800,1500,0,0,0,0)' - (x,y size, x,y dock loc, theta1, theta2), map,roomba roatation")
- floorplan is of the form: '("res/first_floor.jpg",0,0,1.0,0)' - (filename, x, y, scale, roatation, transparency)
"""
myroomba.enable_map(enable=True, 
                    mapSize="(932, 1999, 205, -160, 1, 0, 0, 0 )", 
                    mapPath="./", 
                    iconPath="./res",
                    floorplan = '("res/first_floor.jpg",0,0,1.0,0,0.5)',
                    roomba_size=(15,15),
                    draw_edges = 10)  #enable live maps, class default is no maps

try:
    if broker is not None:
        myroomba.setup_mqtt_client(broker, 1883, user, password, '/roomba/feedback') #if you want to publish Roomba data to your own mqtt broker (default is not to) if you have more than one roomba, and assign a roombaName, it is addded to this topic (ie /roomba/feedback/roombaName)
    #finally connect to Roomba - (required!)
    myroomba.connect()

    print("<CMTRL C> to exit")
    print("Subscribe to /roomba/feedback/# to see published data")
    
    loop.run_forever()

except (KeyboardInterrupt, SystemExit):
    print("System exit Received - Exiting program")
    myroomba.disconnect()
finally:
    print("Bye!")
    myroomba.disconnect()
