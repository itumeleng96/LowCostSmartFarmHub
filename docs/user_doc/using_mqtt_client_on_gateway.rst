Using the MQTT Client on the gateway to publish and subscribe to Broker
=======================================================================

The gateway publishes data and recieves commands from the MQTT broker using the methods described below.

.. warning::
  Ensure that the Cloud Applications are runnning or that the provided broker address is a valid 
  MQTT broker address ready to recieve data from gateway


Connect to MQTT broker
----------------------
With the gateway connected to the internet, the gateway can communicate with the server using
the methods below.


**Connect Gateway to MQTT broker**

.. code:: python

  [...]

  # Instantiate a Gateway device object
  gateway = Gateway("RPI 3B+","Farm location 1")

  gateway.mqtt_connect(client_id="xvsvs",broker='www.mosquitto-broker.com',port=1883)

  #returns a MQTT client
  [...]


Publish all devices information to MQTT broker
----------------------------------------------
The gateway can publish all the information from the devices on the sensor network

**Publish All Sensor Data to MQTT broker**

.. code:: python

  [...]

  # Instantiate a Gateway device object
  gateway = Gateway("RPI 3B+","Farm location 1")

  client=gateway.mqtt_connect(client_id="xvsvs",broker='www.mosquitto-broker.com',port=1883)
  
  client.publish()

  [...]