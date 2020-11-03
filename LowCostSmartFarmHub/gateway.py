#RPI Gateway

'''Pin connection for sensors,actuators and Coordinator Node
   Pin 1        : 3.3V <--->Sensor 1,2,3 (VCC)
   Pin 2        : 5V   <--->Low Voltage Actuator
   Pin 11,13,15 : GPIO <--->Digital Sensor Inputs
   Pin 9,30     : GND  <--->Sensor and Actuator GND
   Pin 8 and 10 : UART <--->UART Xbee 
'''

from  sensor import Sensor
from  actuator import Actuator
from  nodeDevice import NodeDevice
import  time
from    digi.xbee.devices   import XBeeDevice
import  serial
import  json
import requests
from paho.mqtt import client as mqtt_client
import RPi.version
import csv
import logging
log = logging.getLogger()


class Gateway:
    '''This class provides functionality for the Gateway Device'''

    def __init__(self,deviceName=None,location=None,sensors=[],actuators=[],nodeDevices=[],panID=None):
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
    def get_node_device(self,mac_address,discovered_devices):
        """
        Looks for node device with the specified mac address on the network
        
           Args:
              mac_address: unique 64 Bit address of XBee3 modules
           Returns:
              The node device
        """
        for i in range(len(discovered_devices)):
          if(str(discovered_devices[i].get_64bit_addr())==str(mac_address)):
            return discovered_devices[i]
   
    def check_node_device(self,xbee_object):
        for nodes in self.nodeDevices:
           if(str(nodes.XBeeObject.get_64bit_addr())==str(xbee_object.get_64bit_addr())):
              return True
        return False
    
    def add_node_device(self,xbee_object,node_name,node_type,sensor,actuator):
        """
        Adds the node device and its devices to network
        
        Args: 
               node(NodeDevice)
               sensor(Sensor)
               actuator(Actuator)
        """
        #First Check if the Node is already in the list
        if(self.check_node_device(xbee_object)==False) :
          if(sensor!=""):
            node=NodeDevice(node_name,node_type,xbee_object.get_64bit_addr())
            node.XBeeObject=xbee_object
            node.sensors=[sensor]
            self.nodeDevices.append(node)
          elif(actuator!=""):
            node=NodeDevice(node_name,node_type,xbee_object.get_64bit_addr()) 
            node.XBeeObject=xbee_object 
            node.add_sensor(actuator)
            self.nodeDevices.append(node)

          return 0

        if(self.check_node_device(xbee_object)):
          for node_dev in self.nodeDevices:
            if(str(node_dev.XBeeObject.get_64bit_addr())==str(xbee_object.get_64bit_addr())):
              if(sensor!=""):
                node_dev.add_sensor(sensor)
              elif(actuator!=""):
                node_dev.add_actuator(actuator)
          return 1

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

    def publish(self,client,interval):
        """
        Publishes all the devices infromation to the broker specified
        
        Args:
            client(mqtt_client):The MQTT client object
        """
       
        while True:
            count_sensors=0
            count_actuators=0
            count_nodes=0

            #self.detect_devices(self.localXBee,True,"devices.csv")

            for sensor in self.sensors:
                self.publish_sensor_info(client,sensor)
                count_sensors+=1
            for actuator in self.actuators:
                self.publish_actuator_info(client,actuator)
                count_actuators+=1
            for node_device in self.nodeDevices:
                count_nodes+=1
                self.publish_power_info(client,node_device)
                for sensor_in_node in node_device.sensors:
                    sensor_in_node.read_analog_xbee_sensor(node_device.XBeeObject)
                    self.publish_sensor_info(client,sensor_in_node,node_device)
                    count_sensors+=1
                for actuator_in_node in node_device.actuators:
                    self.publish_actuator_info(client,actuator)
                    count_actuators+=1

            self.publish_device_list(client,"Actuators",count_actuators)
            self.publish_device_list(client,"Sensors",count_sensors)
            self.publish_device_list(client,"Node-devices",count_nodes)
            print("Devices on the Wireless Sensor Network......")
            print("actuators",count_actuators)
            print("sensors",count_sensors)
            print("nodes",count_nodes)
            time.sleep(interval)

    def publish_sensor_info(self,client,sensor:Sensor,node:NodeDevice):
        """
        Publishes the provided sensor infromation to the broker specified

        Args:
            client(mqtt_client):The MQTT client object
            sensor(Sensor): The sensor object with all the attributes of the sensor
        """
        sensor.read_analog_xbee_sensor(node.XBeeObject)
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
        payload_dict={"node_name":node_device.nodeName,"battery_type":"Lithium-ion","node_id":str(node_device.macAddress),"data":{"value":node_device.get_battery_level(),"units":"percentage"}}
        payload=json.dumps(payload_dict)

        topic = 'data/myfarm/dorm-room/power/'
        result = client.publish(topic,payload,2)

        # result: [0, 1]
        status = result[0]
        if status == 0:
            print("Send",payload," to topic ",topic)
        else:
            print("Failed to send message to topic ",topic)

    def publish_device_list(self,client,device,number_of_devices):
        """
        Publishes the number of the specified devices
     
        Args:
        """
        payload_dict={"device_name":device,"data":{"value":number_of_devices}}
        payload=json.dumps(payload_dict)

        topic = 'data/myfarm/dorm-room/devices/'

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
        payload_dict={"sensor_name":actuator.actuatorName,"sensor_id":actuator.actuatorID,"sensor_connection":"digital","data":{"value":actuator.get_last_value()}}
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

    def detect_devices(self,coordinator,add_devices,csv_path='/'):
        """
        This function detects all devices connected to the Gateway

        Args:
            add_devices(Boolean): if true, it automatically adds the devices to the gateway
            csv_path(String) : path to a CSV file that defines the devices on network

        Returns:
            A list of all devices on gateway (Actuators,Sensors, Local Nodes)
        """

        #GPIO Line Detection - I2C and Digital 
        hub_devices=[]

        #Add Local XBee to list of Devices
        hub_devices.append(self.localXBee)
        #Discover Remote Zigbee Devices
        devices=self.discover_zigbee_devices()
        #create Nodes and Add them to system

        for device in devices:
            hub_devices.append(device)

        #Read CSV File and assign information to devices
        with open(csv_path) as csv_file:
            csv_reader=csv.reader(csv_file,delimiter=',')
            line_count=0

            for line  in csv_reader:
                if line_count==0:
                    print("Reading CSV file")
                    line_count+=1
                else:
                    #Get The device  attributes
                    #Create sensors
                    if(line[0]=="gateway"): #Add sensor or actuator to gateway
                        if(line[2]=="sensor"):
                            sensor=Sensor(line[3],line_count,line[4],line[9],line[7],line[10],line[5])
                            self.add_sensor(sensor)
                        elif(line[2]=="actuator"):
                            actuator=Actuator(line[3],line_count,line[4],line[9],int(line[10]),[0])
                            self.add_actuator(actuator)
                    
                    #Create Node Devices
                    elif(line[0]=="coordinator" or line[0]=="router"):
                        #check if the mac addresses are the same
                        xbee_object=self.get_node_device(line[6],hub_devices) 

                        if(line[2]=="sensor"):
                            sensor=Sensor(line[3],line_count,line[4],line[9],line[7],line[10],line[5])
                            self.add_node_device(xbee_object,line[1],line[0],sensor,"")

                        elif(line[2]=="actuator"):
                            actuator=Actuator(line[3],line_count,line[4],line[9],line[10],[0])
                            self.add_node_device(xbee_object,line[1],line[0],"",actuator)
 
                    line_count+=1

        return hub_devices
