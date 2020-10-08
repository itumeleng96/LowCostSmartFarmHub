#RPI3B+ Gateway

'''Pin connection for sensors,actuators and Coordinator Node
   Pin 1        : 3.3V <--->Sensor 1,2,3 (VCC)
   Pin 2              : 5V   <--->Low Voltage Actuator
   Pin 11,13,15 : GPIO <--->Digital Sensor Inputs
   Pin 9,30     : GND  <--->Sensor and Actuator GND
'''

import sensor
import actuator
import nodeDevice
from digi.xbee.devices import XBeeDevice

class Gateway:
    
    '''This class provides functionality for the Gateway Device'''
    deviceName:str
    sensors:[]
    actuators:[]
    location:str
    nodeDevices:[]
    pamID:str

    def __init__(self,deviceName,sensors,actuators,location,nodeDevices,panID):
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
        
    #def    searchForZigbeeDevices(self):
        # Some Code to Send to The coordinator Node to get search for New Devices
    
    #Connect to Local Zigbee Device (Serial Port)
    def connectNewStreamUART(self,comPort):
        # Code to allow the RPI3B+ to communicate with Coordinator Through USB-UART         
        localXbee=XbeeDevice(comPort,9600)  #With Baudrate:9600
        localXbee.open() 

    #Update Device Nodes Firmware
    #Def updateFirmware():
