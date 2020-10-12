

#Pin Specification for Xbee3 Node Device
#VCC 
#GND
#Pin 2      : DIO13     <---->UART Data Out
#Pin 3      : DIO14     <---->UART Data In
#Pin 17-20  : DIO3-DIO0 <---->Sensor Analog/Digital Input

#This Class defines the Node Devices on the Network

from    digi.xbee.devices   import XBeeDevice

class NodeDevice:
    nodeName:str
    nodeType:str
    location:str
    sensors:[]
    actuators:[]
    macAddress:str
    batteryLevel:str
    XbeeObject:XBeeDevice

    # Initialize Node Object	
    def __init__(self,nodeName,nodeType,macAddress,sensors=None,actuators=None,location=None,batteryLevel=None):
        self.nodeName=nodeName              #Xbee3 node,zigbee device
        self.nodeType=nodeType              #Coordinator,End-Device,Router
        self.location=location              #Location of node device,e.g Farm1 lat:28298383 lng:937373
        self.sensors=sensors                #A list of all the sensors connected on the Node
        self.actuators=actuators            #A list of all the actuators connected on the Node
        self.batteryLevel=batteryLevel      # Device battery level in decimal
        self.macAddress=macAddress          # Every Device or Node on network has MAC Address

    # Add sensor to Node Device
    def addSensor(self,sensor):
        self.sensors.append(sensor)
        #Trigger some event to read sensor Value and send to Broker

    #Remove Sensor from Node Device
    def removeSensor(self,sensorID):
        for sensor in self.sensors:
            if sensor.sensorID==sensorID:
                self.sensors.remove(sensor)

    # Add Actuator to Node Device
    def addActuator(self,actuator):
        self.actuators.append(actuator)
        #Trigger some event to read sensor Value and send to Broker

    #Remove Sensor from Node Device
    def removeActuator(self,actuatorID):
        for actuator in self.actuators:
            if actuator.actuatorID==actuatorID:
                self.actuators.remove(actuator)
