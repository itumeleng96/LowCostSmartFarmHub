XBee terminology
================

This section covers basic LowCostSmartFarmHub concepts and terminology.The various modules and classes 
used in the API will make references to these terms.


Gateway device
--------------
A gateway is a device that acts as the middle-man between the internet and the wireless-sensor network 
made up of radio modules.The gateway has to be connected to the internet through WIFI or ethernet to transmit 
local data to the internet.


Actuator
--------
Any device that is capable of recieving commands and converting them to an electrical signal for lighting or any other
mechanical movement.This device is usually connected to the Node Devices(RF modules) or to the gateway directly.

Sensor
------
Any device capable of measuring and gathering environmental data in a farm and communicating with the gateway or node-device.
This device can be I2C,analog or digital sensor.


Node-device
-----------
Any device that can act as node in the smart-farm wireless network. This can be any Zigbee RF module or a zigbee device in the network.

ZigBee RF modules
-----------------

A radio frequency (RF) module is a small electronic circuit used to transmit
and receive radio signals on different frequencies.The RF modules used in this API are 
from Digi-XBee and they are the XBee3 Through Hole RF Modules.




Radio module operating modes from Digi-XBee
------------------------------------------- 

The operating mode of an XBee radio module establishes the way a user, or any
microcontroller attached to the XBee, communicates with the module through the
Universal Asynchronous Receiver/Transmitter (UART) or serial interface.

Depending on the firmware and its configuration, the radio modules can work in
three different operating modes:

* Application Transparent (AT) operating mode
* API operating mode
* API escaped operating mode

In some cases, the operating mode of a radio module is established by the
firmware version and the firmware's AP setting. The module's firmware version
determines whether the operating mode is AT or API. The firmware's AP setting
determines if the API mode is escaped (**AP** = 2) or not (**AP** = 1). In
other cases, the operating mode is only determined by the AP setting, which
allows you to configure the mode to be AT (**AP** = 0), API (**AP** = 1) or
API escaped (**AP** = 2).

