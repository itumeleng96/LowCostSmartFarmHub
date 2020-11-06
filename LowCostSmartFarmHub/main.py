import paho.mqtt.client as mqtt
from    gateway import  Gateway
import time
from    nodeDevice import NodeDevice
from    sensor  import Sensor
from    actuator import Actuator
import  json
import  random

#The callback for when the client receives a CONNACK response from the server.
gateway=Gateway()

def main():
    #Initialize Gateway object from gateway
    print("Checking for Coordinator device and initializing network")
    connected=gateway.connect_stream_uart("/dev/serial0",9600)
    if (connected):
      devices=gateway.detect_devices(gateway.localXBee,True,"devices.csv")
      print("The Node Devices Detected")
      print(devices)
      
      print("Publishing to Broker every minute and Waiting for cmd messages")

      client_id = f'python-mqtt-{random.randint(0, 1000)}'
      mqtt_client=gateway.connect_mqtt(client_id,'localhost',1883)
      mqtt_client.loop_start()
      gateway.publish(mqtt_client,60)

    else:
      print("Failed to connect to Coordinator")

    print("Publishing to Broker every minute and Waiting for cmd messages")

if __name__ == '__main__':
    print('Running smart Farm Hub')
    main()
