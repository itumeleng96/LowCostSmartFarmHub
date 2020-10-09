#RPI3B+ Gateway

'''Pin connection for sensors,actuators and Coordinator Node
   Pin 1        : 3.3V <--->Sensor 1,2,3 (VCC)
   Pin 2        : 5V   <--->Low Voltage Actuator
   Pin 11,13,15 : GPIO <--->Digital Sensor Inputs
   Pin 9,30     : GND  <--->Sensor and Actuator GND
   USB          : USB  <--->UART Xbee 
'''

import sensor
import actuator
import nodeDevice
import time
from digi.xbee.devices import XBeeDevice

class Gateway:
    
    '''This class provides functionality for the Gateway Device'''
    deviceName:str
    sensors:[]
    actuators:[]
    location:str
    nodeDevices:[]            #All the Node Devices(Xbee) in the Network 
    panID:str                 #The Unique Zigbee Network Identifier
    localXBee:XBeeDevice      #The Local Zigbee device used as Coordinator through serial Port

    def __init__(self,deviceName,sensors,actuators,location,nodeDevices,panID=None):
        self.deviceName=deviceName
        self.sensors=sensors
        self.actuators=actuators
        self.location=location
        self.nodeDevices=nodeDevices
        self.panID=panID
	
    def addSensor(self,sensor:sensor):
        self.sensors.append(sensor)
    #def    removeSensor(self,sensor.sensorID):
        #

    def  addActuator(self,actuator:actuator):
        self.actuators.append(actuator)
        
    #def    removeActuator(self,actuator.actuatorID):
        #
        
    def addNewZigbeeDevice(self,nodeDevice:nodeDevice):
        self.nodeDevices.append(nodeDevice)
        
    #Connect to Local Zigbee Device (Serial Port)
    def connectNewStreamUART(self,comPort):
        # Code to allow the RPI3B+ to communicate with Coordinator Through USB-UART         
        localXBee=XBeeDevice(comPort,9600)  #With Baudrate:9600
        localXBee.open()
        self.panID=localXBee.get_pan_id()   #Set the PanID
    
    #Discover Devices on the Network
    def discoverZigbeeDevices(self):
        #Get Xbee network object from the Xbee Device
        xnet=self.localXBee.get_network()
        #Start the discovery process and wait for it to be over
        while xnet.is_discovery_running():
            time.sleep(0.5)

        #Get the List of Devices added to the Network and Add to Node Devices        
        devices = xnet.get_devices()
        print(devices)
        #....
        
    #Update Xbee Devices  Firmware
    #def updateFirmware():
        #Update Local Xbee Device 
        #Update Remote Xbee Device
