

#Pin Specification for Xbee3 Node Device
#VCC 
#GND
#Pin 2      : DIO13     <---->UART Data Out
#Pin 3      : DIO14     <---->UART Data In
#Pin 17-20  : DIO3-DIO0 <---->Sensor Analog/Digital Input

#This Class defines the Node Devices on the Network



class NodeDevice:

    # Initialize Node Object

    def __init__(self,nodeName,sensors,actuators,location,nodeType,batteryLevel,macAddress):
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
    def addActuator(self,sensor):
        self.actuators.append(actuators)
        #Trigger some event to read sensor Value and send to Broker

    #Remove Sensor from Node Device
    def removeSensor(self,actuatorID):
        for actuator in self.actuator:
            if actuator.actuatorID==actuatorID:
                self.actuator.remove(actuator)
    
    #Connect Node to UART Stream for Communication with uC or RPI 
    def connectUARTStream(self,usb_connect,RX_pin,TX_pin):
        #Trigger Transmission Between Coordinator Node and Gateway
        #
        #

        
