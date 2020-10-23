import paho.mqtt.client as mqtt
from    LowCostSmartFarmHub.gateway import  Gateway
import time
from    LowCostSmartFarmHub.nodeDevice import NodeDevice
from    sensor  import Sensor
import  json
#The callback for when the client receives a CONNACK response from the server.

gateway=Gateway("RPI","farm1",[],[],[],"")
state="off"
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("cmd/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global state
    print(msg.topic+" "+str(msg.payload))
    if(msg.topic =="cmd/myfarm/dorm-room/gateway/switch/"):
      if(state=="off"):
        print("Switching light on Gateway")
        gateway.control_actuator_on_gateway(18,"on")
        state="on"
      elif (state=="on"):
        print("switching light off")
        gateway.control_actuator_on_gateway(18,"off")
        state="off"
def main():

    #Initialize Gateway object from gateway
    print("Connecting to Local XBee through UART")
    gateway.connectNewStreamUART("/dev/serial0")
    
    devices=gateway.discoverZigbeeDevices()
    print(devices)

    #Remote Node Device
    sensor1=Sensor("Soil Moisture Sensor","XCVE","Soil Moisture","Measures soil moisture in percentage","%")
    node_device_1=NodeDevice("Remote Xbee Module","end-device","GBSJDMMD",sensor1)
    node_device_1.XbeeObject=devices[0]
    sensor_value=node_device_1.read_analog_sensor(0,sensor1,100)
    print("Soil Moisture Sensor:",sensor_value,"%")
    
    #Local Node Device 
    sensor2=Sensor("Temperature Sensor","BFNND","Temperature","Measures Temperature in degrees celcius","degrees")
    node_device_2=NodeDevice("Local Xbee Module","end-device","GBSJDMMD",sensor2)
    node_device_2.XbeeObject=gateway.localXBee
    sensor_value2=node_device_2.read_analog_sensor(0,sensor1,50)
    print("Temperature Sensor:",sensor_value2,"degrees")

    sensor3=Sensor("Humidity Sensor","BFNND","Humidity","Measures Humidity in percentage","%")
    sensor_value3=node_device_2.read_analog_sensor(1,sensor3,100)
    print("Humidity Sensor:",sensor_value3,"%")


    print("Connecting To MQTT Broker")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    #Connecting to MQTT Broker
    client.connect("localhost", 1883, 60)
    print("Publishing to Broker every minute")
    while True:
      #Read Sensor Values
      sensor_value=node_device_1.read_analog_sensor(0,sensor1,100)
      sensor_value2=node_device_2.read_analog_sensor(0,sensor1,50)
      sensor_value3=node_device_2.read_analog_sensor(1,sensor3,100)

      payload_dict={"sensor_name":sensor1.sensorName,"sensor_id":sensor1.sensorID,"sensor_connection":"ADC","data":{"value":sensor_value,"units":sensor1.unit_of_measure}}
      payload=json.dumps(payload_dict)
    
      payload_dict1={"sensor_name":sensor2.sensorName,"sensor_id":sensor2.sensorID,"sensor_connection":"ADC","data":{"value":sensor_value2,"units":sensor2.unit_of_measure}}
      payload1=json.dumps(payload_dict1)
    
      payload_dict2={"sensor_name":sensor3.sensorName,"sensor_id":sensor3.sensorID,"sensor_connection":"ADC","data":{"value":sensor_value3,"units":sensor3.unit_of_measure}}
      payload2=json.dumps(payload_dict2)
    
      client.publish("data/myfarm/dorm-room/soil-sensor/moisture",payload,2)
      client.publish("data/myfarm/dorm-room/temperature-sensor/temperature",payload1,2)
      client.publish("data/myfarm/dorm-room/humidity-sensor/humidity",payload2,2)
      
      time.sleep(60)    #Sleep for a minute

if __name__ == '__main__':
    print('Testing MQTT Client Functions')
    main()
