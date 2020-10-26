import paho.mqtt.client as mqtt
from    LowCostSmartFarmHub.gateway import  Gateway
import time
from    LowCostSmartFarmHub.nodeDevice import NodeDevice
from    sensor  import Sensor
import  json
#The callback for when the client receives a CONNACK response from the server.

gateway=Gateway("RPI","farm1",[],[],[],"")

def main():

    #Initialize Gateway object from gateway
    print("Connecting to Local XBee through UART")
    gateway.connectNewStreamUART("/dev/serial0")
    
    devices=gateway.discoverZigbeeDevices()
    print("Remote Xbee Devices: ",devices)

    #Initialize all sensors on the network 
    sensor1=Sensor("Soil Moisture Sensor","XCVE","Soil Moisture","Measures soil moisture in percentage","%")
    node_device_1=NodeDevice("Remote Xbee Module","end-device","GBSJDMMD",sensor1)
    node_device_1.XbeeObject=devices[0]

    sensor2=Sensor("Temperature Sensor","BFNND","Temperature","Measures Temperature in degrees celcius","degrees")
    node_device_2=NodeDevice("Local Xbee Module","end-device","GBSJDMMD",sensor2)
    node_device_2.XbeeObject=gateway.localXBee

    sensor3=Sensor("Humidity Sensor","BFNND","Humidity","Measures Humidity in percentage","%")
    sensor_value3=node_device_2.read_analog_sensor(1,sensor3,100)


    print("Publishing to Broker every minute")

    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    mqtt_client=gateway.connect_mqtt(client_id,'localhost',1883)
    
    while True:
      #Read Sensor Values
      sensor_value=node_device_1.read_analog_sensor(0,sensor1,100)
      gateway.publish_sensor_info(mqtt_client,sensor1)

      sensor_value2=node_device_2.read_analog_sensor(0,sensor1,50)
      gateway.publish_sensor_info(mqtt_client,sensor2)
      
      sensor_value3=node_device_2.read_analog_sensor(1,sensor3,100)
      gateway.publish_sensor_info(mqtt_client,sensor3)

      time.sleep(60)    #Sleep for a minute

if __name__ == '__main__':
    print('Testing MQTT Client Functions')
    main()
