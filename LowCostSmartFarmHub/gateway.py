#RPI Gateway

'''Pin connection for sensors,actuators and Coordinator Node
   Pin 1        : 3.3V <--->Sensor 1,2,3 (VCC)
   Pin 2        : 5V   <--->Low Voltage Actuator
   Pin 11,13,15 : GPIO <--->Digital Sensor Inputs
   Pin 9,30     : GND  <--->Sensor and Actuator GND
   Pin 8 and 10 : UART <--->UART Xbee 
'''

from .sensor import Sensor
from .actuator import Actuator
from .nodeDevice import NodeDevice
import  time
from    digi.xbee.devices   import XBeeDevice
import  serial
import  json
import requests
from paho.mqtt import client as mqtt_client
import RPi.version
import logging
log = logging.getLogger()


class Gateway:
    '''This class provides functionality for the Gateway Device'''

    def __init__(self,deviceName=None,location=None,sensors=None,actuators=None,nodeDevices=None,panID=None):
        self.deviceName=deviceName
        self.sensors=sensors
        self.actuators=actuators
        self.location=location
        self.nodeDevices=nodeDevices
        self.panID=panID
        self.create_gateway()

    def create_gateway(self):
        """
        This function gets the model information of gateway and the location of the device
        from the internet
        """

        #Get Device information
        device_info = RPi.version.info
        self.deviceName="RPI "+device_info['type']
        
        #Get Device Location approximation
        url = 'https://extreme-ip-lookup.com/json/'
        r = requests.get(url)
        data = json.loads(r.content.decode())
        self.location=data['city']

        #instantiate Gateway attributes
        self.actuators=[]

    def read_gateway_info(self):
        """
        This function returns the device information in a dictionary format

        Returns:
            A dictionary with all the device information
        """
        gateway_info={
                      'device_name':self.deviceName,
                      'location':self.location,
                      'sensors':self.sensors,
                      'actuators':self.actuators,
                      'node_devices':self.nodeDevices
                     }
        
        return gateway_info

    def add_sensor(self,sensor:Sensor):
        """
        Adds a sensor directly to the gateway Device

            Args:
                sensor(Sensor): The sensor object with all the sensor attributes
            
            Returns: 
                A list of all the sensors connected directly to the gateway
        """
        self.sensors.append(sensor)

    def add_actuator(self,actuator:Actuator):
        """
        Adds an Actuator directly to the gateway Device

            Args:
                actuator(Actuator): The actuator object with all the actuator attributes
            
            Returns: 
                A list of all the actuators connected directly to the gateway
        """
        self.actuators.append(actuator)

    def connect_stream_uart(self,comPort,baud_rate):
        """
		Function for opening serial communication Port between RPI and  XBee Device
		Args:
			com_port (String): The serial port where the Coordinator Device is connected to on the Gateway
		Returns:
			None
    	"""
        localXBee=XBeeDevice(comPort,baud_rate)  

        try:
            localXBee.open()
            self.panID=localXBee.get_pan_id()        #Set the PanID
            self.localXBee=localXBee
            return True
        
        except:
            return False


    def discover_zigbee_devices(self):
        """
        Discovers new zigbee devices on the zigbee network 

		Args:
            self
		Returns:
		    A list of the Discovered XBee Devices
        """
        #Get Xbee network object from the Xbee Device
        xnet=self.localXBee.get_network()
        #Clear List of of Devices for Clean Discovery
        xnet.clear()
        #Start the discovery process and wait for it to be over
        
        xnet.start_discovery_process()
        while xnet.is_discovery_running():
            time.sleep(1.5)

        #Get the List of Devices added to the Network and Add to Node Devices        
        devices = xnet.get_devices()
        xnet.add_remotes(devices)
        return  devices

    def publish(self,client):
        """
        Publishes all the devices infromation to the broker specified
        
        Args:
            client(mqtt_client):The MQTT client object

        """

    def publish_sensor_info(self,client,sensor:Sensor):
        """
        Publishes the provided sensor infromation to the broker specified

        Args:
            client(mqtt_client):The MQTT client object
            sensor(Sensor): The sensor object with all the attributes of the sensor
        """
        payload_dict={"sensor_name":sensor.sensor_name,"sensor_id":sensor.sensor_id,"sensor_connection":"ADC","data":{"value":sensor.get_sensor_value(),"units":sensor.unit_of_measure}}
        payload=json.dumps(payload_dict)

        topic = 'data/myfarm/dorm-room/sensor/'+sensor.sensor_name+"/"

        result = client.publish(topic,payload,2)

        # result: [0, 1]
        status = result[0]
        if status == 0:
            print("Send",payload," to topic ",topic)
        else:
            print("Failed to send message to topic ",topic)
    
    def publish_power_info(self,client,node_device:NodeDevice):
        """
        Publishes the provided node device's battery infromation to the broker specified

        Args:
            client(mqtt_client):The MQTT client object
            nodeDevice(nodeDevice): The node Device object with all the attributes of the node
        """
        payload_dict={"node_name":node_device.nodeName,"battery_type":"Lithium-ion","node_id":node_device.macAddress,"data":{"value":node_device.batteryLevel,"units":"percentage"}}
        payload=json.dumps(payload_dict)

        topic = 'data/myfarm/dorm-room/power/'+node_device.nodeName+"/"

        result = client.publish(topic,payload,2)

        # result: [0, 1]
        status = result[0]
        if status == 0:
            print("Send",payload," to topic ",topic)
        else:
            print("Failed to send message to topic ",topic)


    def publish_actuator_info(self,client,actuator:Actuator):
        """
        Publishes the provided sensor infromation to the broker specified

        Args:
            client(mqtt_client):The MQTT client object
            sensor(Sensor): The sensor object with all the attributes of the sensor
        """
        payload_dict={"sensor_name":actuator.actuatorName,"sensor_id":actuator.actuatorID,"sensor_connection":"DIO","data":{"value":actuator.get_last_value()}}
        payload=json.dumps(payload_dict)

        topic = 'data/myfarm/dorm-room/actuator/'+actuator.actuatorName+"/"

        result = client.publish(topic,payload,2)

        # result: [0, 1]
        status = result[0]
        if status == 0:
            print("Send",payload," to topic ",topic)
        else:
            print("Failed to send message to topic ",topic)
    
    def parse_mqtt_message(self,msg):
        """
        This function gets the MQTT cmd message and passes 
        it on to the relevant node or device
        Args:
            msg: The message payload from MQTT broker
        """
        print("Parsing message from MQTT broker")
        self.actuators[0].control_ws28x1_light()

    def connect_mqtt(self,client_id,broker,port):
        """
        This function connects to the MQTT broker

        Args:
            client_id(int) : unique identifier of MQTT client
            broker (string): broker address
            port (int) : The port where the mqtt broker is running
        
        Returns:
            mqtt client 
        """
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                client.subscribe("cmd/#")   #Subscribe to Commands from MQTT broker
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        
        def on_message(client, userdata, msg):
            print("recieved message")
            print(msg.topic+" "+str(msg.payload))
            self.parse_mqtt_message(msg)

        # Set Connecting Client ID
        client = mqtt_client.Client(client_id)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(broker, port)
        return client

    def detect_devices(self,add_devices):
        """
        This function detects all devices connected to the Gateway

        Args:
            add_devices(Boolean): if true, it automatically adds the devices to the gateway

        Returns:
            A list of all devices on gateway (Actuators,Sensors, Local Nodes)

        """

        #GPIO Line Detection - I2C and Digital
        

        #Zigbee Devices Detection - check local and remote
        connected=self.connect_stream_uart("/dev/serial0",9600)
        if connected:
            #Discover Remote Zigbee Devices
            devices=self.discover_zigbee_devices()
            #create Nodes and Add them to system
            log.info("This are the devices:",devices)

            if add_devices:
                for device in devices:
                    self.append(device)
        else:
            log.critical("No Coordinator Device on Gateway")
        
