import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import json



#Provide your IBM Watson Device Credentials
organization = "ef5o1a"
deviceType = "AirpollutionIOT"
deviceId = "1282"
authMethod = "token"
authToken = "9876543210"


# Initialize the device client.

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data['command'])


        if cmd.data['command']=='lighton':
                print("LIGHT ON IS RECEIVED")
                
                
        elif cmd.data['command']=='lightoff':
                print("LIGHT OFF IS RECEIVED")
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        co2=random.randint(0,100)
        nh3=random.randint(100,200)
        T=random.randint(-20,55)
        H=random.randint(0,60)
        name='vijayawada'
        #Send Temperature & Humidity to IBM Watson
        data = {"d":{ 'Location':name,'temperature' : T, 'humidity': H ,'carbondioxide': co2,'Nitrogen':nh3}}
        #print data
        def myOnPublishCallback():
            print ("Published Location= %s %%" %name, "Nitrogen = %s %%" % nh3,"Temperature = %s C" % T, "Humidity = %s %%" % H, "carbondioxide = %s C" % co2, "to IBM Watson")

        success = deviceCli.publishEvent("Data", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(5)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
