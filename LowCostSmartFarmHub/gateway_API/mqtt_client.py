import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
# To create a MQTT client you must provide broker IP and Port

class Client:
    broker_IP:str
    port:int

    def __init__(self,broker_IP,port):
        self.broker_IP=broker_IP
        self.port=port
        #mqtt paho-client object 
        self.client=mqtt.Client()
        self.client.on_connect = on_connect()
        self.client.on_message = on_message()
        self.client.on_publish = on_publish()
        self.client.connect(self.broker,60)
        self.client.loop_forever()


    #The Callback for after connecting to the broker
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("SensorNode1/DHT11")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    # This callback is called everytime the client publishes a message
    def on_publish(client,userdata,result)
        print("Data published ...\n")
        pass 

    def subscribeToTopic(self,topic:str)
        self.client.subscribe(topic)
    
    def sendMessageToTopic(self,topic,message_payload)
       self.client.publish(topic,message_payload)


