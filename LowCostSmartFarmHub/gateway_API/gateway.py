#RPI:3B+ Gateway

'''Pin connection for sensors,actuators and Coordinator Node
   Pin 1        : 3.3V <--->Sensor 1,2,3 (VCC)
   Pin 2        : 5V   <--->Low Voltage Actuator
   Pin 11,13,15 : GPIO <--->Digital Sensor Inputs
   Pin 9,30     : GND  <--->Sensor and Actuator GND
   USB          : USB  <--->UART Xbee 
'''

import  sensor
import  actuator
from    nodeDevice import  NodeDevice
import  time
from    digi.xbee.devices   import XBeeDevice

class Gateway:
    '''This class provides functionality for the Gateway Device'''
    deviceName:str
    sensors:[]
    actuators:[]
    location:str
    nodeDevices:[]              #All the Node Devices(Xbee) in the Network
    panID:str                   #The Unique Zigbee Network Identifier
    localXBee:XBeeDevice        #The Local Zigbee device used as Coordinator through serial Port

    def __init__(self,deviceName,location,sensors=None,actuators=None,nodeDevices=None,panID=None):
        self.deviceName=deviceName
        self.sensors=sensors
        self.actuators=actuators
        self.location=location
        self.nodeDevices=nodeDevices
        self.panID=panID
    
    def addNewZigbeeDevice(self,nodeName,nodeType,xbeeDevice:XBeeDevice):
        """
        Adds the  Zigbee Device to  the Gateway Node Devices
	        Args:
             	node_name (String): name of zigbee device
             	node_type (String): the type of node-device (end-device,router-device,coordinator-device)
             	xbee_device (XBeeDevice): the xbee device of object if device is a Digi XBee module

        	Returns:
             	List of Node Devices connected to Gateway wirelessly and through the serial Port
        	Raises:
             	XBeeException:if the provided XBee device does not responds to commands
        	"""

        print("Adding Zigbee Device to Network")
        print(xbeeDevice.read_device_info())
        #nodeDevice.macAddress=
        #nodeDevice.XbeeObject=
        #nodeDevice=NodeDevice(nodeName,nodeType)
    
        #self.nodeDevices.append(nodeDevice("","",""))

    def connectNewStreamUART(self,comPort):
        """
		Function for opening serial communication Port between RPI and  XBee Device
		Args:
			com_port (String): The serial port where the Coordinator Device is connected to on the Gateway
		Returns:
			None
		"""
        	
        localXBee=XBeeDevice(comPort,9600)  #With Baudrate:9600
        localXBee.open()
        self.panID=localXBee.get_pan_id()   #Set the PanID
        self.localXBee=localXBee
        return

    def discoverZigbeeDevices(self):
        """
        Discovers new zigbee devices on the zigbee network 

		Args:
            self
		Returns:
		    A list of the Discovered XBee Devices
        """
        #Get Xbee network object from the Xbee Device
        xnet=self.localXBee.get_network()
        xnet.clear()  			   #Clear List of of Devices for Clean Discovery
		#Start the discovery process and wait for it to be over
        xnet.start_discovery_process()
        while xnet.is_discovery_running():
            time.sleep(1.5)
	    
        #Get the List of Devices added to the Network and Add to Node Devices        
        devices = xnet.get_devices()
        return  devices

    #def add_sensor_to_gateway(self,sensor:sensor):
	#def add_sensor_to_node(self,sensor:sensor,nodeName):
    #Some code for configuring IO pins on sensor
    #self.sensors.append(sensor)
    #def removeSensor(self,sensor.sensorID):
    #def  addActuator(self,actuator:actuator):
    #    self.actuators.append(actuator)
    #def   	 removeActuator(self,actuator.actuatorID):

    #RPI Read Function
    #def readGPIOPin():
    
    #def sendCommandGPIOPin():

    #XBee Read and Send Command Functions
    #def readLocalXbeeAnalogPin(Xbee3Pin,XbeeLocalObject):
    #def communicateLocalXbeeDigitalPin(Xbee3Pin,XbeeNodeDevice):
    #def readRemoteXbeeAnalogPin(Xbee3Pin,XbeeNodeDevice):
    #def communicateRemoteXbeeDigitalPin(Xbee3Pin,XbeeNodeDevice):
    
    #Update Xbee Devices  Firmware
    #def updateFirmware():
        #Update Local Xbee Device 
        #Update Remote Xbee Device

    #Initialize Node Device Pin When Sensor is Added and Ping Sensor
    #def addSensorToXbee()

    #Initialize RPI Device Pin when sensor is added

    
    
