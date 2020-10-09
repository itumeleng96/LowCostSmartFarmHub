### Using the Gateway API with Raspberry PI3B+ and Xbee Devices

#### To run the main program (This starts the MQTT client) 
```
    python3 main.py
````
#### Communicate with Xbee3 Coordinator Device Through Serial Port
Get the Communication Port on RPI with the following command
```
  dmesg | grep -i FTDI
```
From the ouput,use the serial port with the GATEWAY connectNewUARTStream() API function
#### To use the Gateway API functions:
