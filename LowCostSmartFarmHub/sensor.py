from    digi.xbee.devices   import XBeeDevice
from    digi.xbee.io    import  IOLine,IOMode
import time
import RPi.GPIO as GPIO
import dht11

class Sensor:
    '''This class provides functionality for the Sensor'''
    
    def __init__(self,sensorName,sensorID,sensorType,description,unit_of_measure,connection_pin,conversion,sensorValues=[]):
        self.sensor_name=sensorName      #Every Sensor on the network has a name
        self.sensor_id=sensorID          #Every Sensor on the network has a unique ID
        self.sensor_type=sensorType      #I2C,ADC,DIO
        self.sensor_values=sensorValues  #[recent sensor values]
        self.description=description    #More information about sensor ,humidity,Temperature
        self.unit_of_measure=unit_of_measure    #The unit of measure (percentage,degrees,grams of water per unit of air)
        self.connection_pin=connection_pin
        self.conversion=conversion
        
    def read_analog_xbee_sensor(self,XbeeDevice:XBeeDevice):
        """
        This provides functionality for getting the sensor value on a Xbee Node

        Args:
            analog_pin_index (Integer) : The analog pin that sensor is connected to on XBee module 0=>DIO0,1->DIO1
            XbeeDevice (XBeeDevice)    : The node device where the sensor is connected
        
        Returns:
            Sensor Value
        """
        sensor_value=0
        #Configure the  pin to analog (Pin must support Analog signal Pin0-Pin3)
        XbeeDevice.set_io_configuration(IOLine.get(int(self.connection_pin)),IOMode.ADC)
        sensor_value=XbeeDevice.get_adc_value(IOLine.get(int(self.connection_pin)))

        #Convert 10 Bit ADC value to relevant value
        sensor_value=100-round(float(sensor_value/1023.0)*int(self.conversion),2) 

        #raise Exception('The selected pin does not support Analog');
        
        self.sensor_values.append(sensor_value)
        return str(sensor_value)

    def read_digital_sensor_dht11(self):
        """
        This function reads the values from the DHT11 sensor
        
        Returns:
             The sensor value
        """
        time.sleep(20) #This ensures that sampling frequency is less than 1 Hz
        GPIO.setmode(GPIO.BCM)
        
        instance = dht11.DHT11(pin = int(self.connection_pin))
        valid=True

        while valid:
          result = instance.read()
          if(str(self.sensor_name)=='DHT11-temperature') and result.is_valid():
              self.sensor_values.append(result.temperature)
              valid=False
          elif(str(self.sensor_name)=='DHT11-humidity') and result.is_valid():
              self.sensor_values.append(result.humidity)
              valid=False

        return 0 

    def read_digital_xbee_sensor(self,xbee_device:XBeeDevice,io_digital_pin):
        """
        This function provides functionality for interfacing with the DHT11 Humidity and Temperature sensor 
        connected to an XBee 3 module

        Args:
            xbee_device (XBee Device): The Xbee module object that represents the XBee module 3 in the network
            io_digital_pin (Integer) : The digital IO pin that the sensor is connected to
        """
    def get_sensor_value(self):
        """
        Gets the most recent sensor value 

        Returns:
            Sensor value
        """
        return self.sensor_values[len(self.sensor_values)-1]
