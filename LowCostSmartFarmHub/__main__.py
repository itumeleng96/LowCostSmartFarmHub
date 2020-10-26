import paho.mqtt.client as mqtt
from    gateway import  Gateway
import time
from    nodeDevice import NodeDevice
from    sensor  import Sensor
import  json
import  random
#The callback for when the client receives a CONNACK response from the server.

gateway=Gateway("RPI","farm1",[],[],[],"")

def main():

    #Initialize Gateway object from gateway
    print("Connecting to Local XBee through UART")
    gateway.connect_stream_uart("/dev/serial0",9600,True)
    
    devices=gateway.discover_zigbee_devices()
    print("Remote Xbee Devices: ",devices)

    #Initialize all sensors on the network 
    sensor1=Sensor("Soil Moisture Sensor","XCVE","Soil Moisture","Measures soil moisture in percentage","%")
    node_device_1=NodeDevice("Remote Xbee Module","end-device","GBSJDMMD",sensor1)
    node_device_1.XbeeObject=devices[0]

    sensor2=Sensor("Temperature Sensor","BFNND","Temperature","Measures Temperature in degrees celcius","degrees")
    node_device_2=NodeDevice("Local Xbee Module","end-device","GBSJDMMD",sensor2)
    node_device_2.XbeeObject=gateway.localXBee

    sensor3=Sensor("Humidity Sensor","BFNND","Humidity","Measures Humidity in percentage","%")


    print("Publishing to Broker every minute")

    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    mqtt_client=gateway.connect_mqtt(client_id,'localhost',1883)
    mqtt_client.loop_start() 
    while True:
      #Read Sensor Values
      sensor_value=sensor1.read_analog_xbee_sensor(node_device_1.XbeeObject,0,100)
      gateway.publish_sensor_info(mqtt_client,sensor1)

      sensor_value2=sensor2.read_analog_xbee_sensor(node_device_2.XbeeObject,0,50)
      gateway.publish_sensor_info(mqtt_client,sensor2)
      
      sensor_value3=sensor3.read_analog_xbee_sensor(node_device_3.XbeeObject,0,100)

      gateway.publish_sensor_info(mqtt_client,sensor3)

      time.sleep(60)    #Sleep for a minute

if __name__ == '__main__':
    print('Testing MQTT Client Functions')
    main()
