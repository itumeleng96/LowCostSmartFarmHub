#RPI3B+ Gateway

#Pin connection for sensors,actuators and Coordinator Node
#Pin 1        : 3.3V <--->Sensor 1,2,3 (VCC)
#Pin 2	      : 5V   <--->Low Voltage Actuator 
#Pin 11,13,15 : GPIO <--->Digital Sensor Inputs
#Pin 9,30     : GND  <--->Sensor and Actuator GND


class Gateway:
	
	#Initialize Gateway Object
	def __init__(self,deviceName,sensors,actuators,location,nodeDevices,panID):
		self.deviceName=deviceName		#Name of the Gateway Device (RPI3b+)
		self.sensors=sensors			#A List of all the sensors connected directly to Gateway
		self.actuators=actuators 		#A List of all the actuators connected directly to Gateway
		self.location=location			#Location of the Gateway
		self.nodeDevices=nodeDevices 		#A list of all the Node Devices connected to the Network
		self.panID=panID 			#Every zigbee network has a PAN ID that all devices in the network share
	
	
	def addSensor(self,sensor:Sensor):	
		self.sensors.append(sensor)
	def removeSensor(self,sensor.sensorID)
		

	def addActuator(self,actuator:Actuator):
		self.actuators.append(actuators)
	
	def removeActuator(self,actuator.actuatorID):
	
	
	def addNewZigbeeDevice(self,nodeDevice:NodeDevice):
		self.nodeDevices.append(NodeDevice)
	
	def searchForZigbeeDevices(self):
		#Some Code to Send to The coordinator Node to get search for New Devices
		#
	def connectNewStreamUART(self):
		#Some code to allow the RPI3B+ to communicate with Coordinator Through USB-UART	 
		#Some connection initialization Code
	def sendDataToBroker(self,topic,payload):
		#Call MQTT client function to publish Data to Broker
		#
	def startMQTTBroker(self):
		#Some Code to call MQTT paho Client Function to start Connection With Broker
	def stopMQTTBroker(self):
		#Some code to stop MQTT Client Connection
		#
	
