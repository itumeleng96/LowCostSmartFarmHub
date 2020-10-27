Configure the Raspberry PI Device
=================================

The LowCostSmartFarmHub  Python Library provides the ability to communicate with 
XBee devices connected to a low-power gateway device that publishes data to a MQTT Broker.

.. warning::
  Communication features described in this topic and sub-topics are only
  applicable for machines like RPI3B+ with UART interfaces connecting to local XBee devices.

Create A gateway and add devices to it
----------------------------------------

The RPI gateway can connect to a  local Xbee Device on the UART interface specified by the user.

** Instantiate the Gateway and connect to local XBee device on UART ** 

.. code:: python

  [...]

  # Instantiate a Gateway device object
  
  gateway = Gateway("RPI 3B+","Farm location 1")

  
  # connect to Local XBee device on UART interface
  
  gateway.connect_uart_stream("COM1",9600,True)


  [...]


The previous methods may fail for the following reasons:

* There is no XBee device on the serial UART interface
  a ``Connection Exception ``.

* Other errors caught as ``XBeeException``:

    * The operating mode of the device is not ``API`` or ``ESCAPED_API_MODE``,
      throwing an ``InvalidOperatingModeException``.
 

```````````````````````````````````````````````````````````````````````

Get and Set Gateway Paramaters
------------------------------
The Gateway Class has various methods that allow the user to set and get certain attributes of the 
gateway.


+---------------------------+--------------------------------------+
| Class Method              | Description                          |
+===========================+======================================+
| read_device_info()        | returns information about gateway    |
+---------------------------+--------------------------------------+
| add_actuator(actuator)    | Adds actuator to the gateway         |
+---------------------------+--------------------------------------+
| add_sensor(Sensor)        | Adds sensor to the gateway           |
+---------------------------+--------------------------------------+




+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
