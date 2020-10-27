
Work with the Raspberry PI Gateway 
====================================

The Gateway Class provides methods to connect to local XBee devices and discover 
remote XBee devices and add them to the gateway using the digi-xbee API  https://github.com/digidotcom/xbee-python

.. warning::
  Ensure that the XBee Coordinator device is connected to the Gateway before 
  executing the discover zigbee devices method

Discover remote Zigbee devices on the same network
--------------------------------------------------
Using the coordinator in API mode, the remote devices can be found using this method

**Instantiate Gateway and Discover Local Devices**

.. code:: python

  [...]

  # Instantiate a Gateway device object
  gateway = Gateway()

  # connect to Local XBee device on UART interface
  gateway.connect_uart_stream("COM1",9600,True)

  devices=gateway.discover_zigbee_devices()

  #devices =[remote xbee1,remote xbee2, e.t.c]

  [...]


Detect all sensors and actuators connected directly to Gateway
--------------------------------------------------------------
This method detects all the devices connected directly to gateway and adds them to the gateway

**Instantiate Gateway and detect Devices on gateway**

.. code:: python

  [...]

  # Instantiate a Gateway device object
  gateway = Gateway()

  #Detect Devices on Gateway
  gateway.detect_devices(add_devices=True)
  
  [...]

