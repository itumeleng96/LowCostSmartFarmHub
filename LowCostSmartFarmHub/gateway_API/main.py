import paho.mqtt.client as mqtt
from gateway import Gateway
import time

#The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("data/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


def main():

    #Initialize Gateway object from gateway
    gateway=Gateway("RPI","farm1",[],[],[],"")
    print("Connecting to Local XBee through UART")
    gateway.connectNewStreamUART("/dev/ttyUSB0")
    print("Searching for Remote Zigbee Devices")
    devices=gateway.discoverZigbeeDevices()
    gateway.control_actuator_on_gateway(32)
    #gateway.addNewZigbeeDevice("Xbee3","End-node",)
    #print(devices)
    #time.sleep(10)
    #print("Connecting To MQTT Broker")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
   # Connecting to MQTT Broker
   # client.connect("192.168.101.148", 1883, 60)
   # client.loop_forever()

if __name__ == '__main__':
    print('Testing MQTT Client Functions')
    main()
