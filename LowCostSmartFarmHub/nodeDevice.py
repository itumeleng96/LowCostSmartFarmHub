

#Pin Specification for Xbee3 Node Device
#VCC 
#GND
#Pin 2      : DIO13     <---->UART Data Out
#Pin 3      : DIO14     <---->UART Data In
#Pin 17-20  : DIO3-DIO0 <---->Sensor Analog/Digital Input

#This Class defines the Node Devices on the Network

from    digi.xbee.devices   import XBeeDevice
from    LowCostSmartFarmHub.sensor  import Sensor

class NodeDevice:
    '''This class represents every node device on the network'''
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

    def add_sensor(self,sensor):
        """
        To add sensors to the node

        Args:
            sensor(Sensor): The sensor Object containing all attributes of the sensor
        
        Returns:
            the new list of sensors
        """
        self.sensors.append(sensor)
        #Trigger some event to read sensor Value and send to Broker

    def remove_sensor(self,sensorID):
        """
        To remove  sensors from the node

        Args:
            sensor(Sensor): The sensor Object containing all attributes of the sensor
        
        Returns:
            the new list of sensors
        
        Throws Exception:
            if the sensor is not in the list
        """
        for sensor in self.sensors:
            if sensor.sensorID==sensorID:
                self.sensors.remove(sensor)

    def add_actuator(self,actuator):
        """
        To add actuators to the node

        Args:
            actuator(Actuator): The actuator Object containing all attributes of the sensor
        
        Returns:
            the new list of actuators
        """
        self.actuators.append(actuator)

    def removeActuator(self,actuatorID):
        """
        To remove  actuators from the node

        Args:
            actuator(Actuator): The actuator Object containing all attributes of the sensor
        
        Returns:
            the new list of actuators
        """
        for actuator in self.actuators:
            if actuator.actuatorID==actuatorID:
                self.actuators.remove(actuator)

     
