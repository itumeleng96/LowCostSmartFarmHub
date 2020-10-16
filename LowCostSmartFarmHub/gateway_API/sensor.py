from    digi.xbee.devices   import XBeeDevice
from    digi.xbee.io    import  IOLine,IOMode
import time

class Sensor:
    sensorName:str
    sensorID:int
    sensorType:str
    sensorValues:[]
    description:str
    unit_of_measure:str
    
    def __init__(self,sensorName,sensorID,sensorType,description,unit_of_measure,sensorValues=None):
        self.sensorName=sensorName      #Every Sensor on the network has a name
        self.sensorID=sensorID          #Every Sensor on the network has a unique ID
        self.sensorType=sensorType      #I2C,ADC,DIO
        self.sensorValues=sensorValues  #[recent sensor values]
        self.description=description    #More information about sensor ,humidity,Temperature
        self.unit_of_measure=unit_of_measure    #The unit of measure (percentage,degrees,grams of water per unit of air)
        
    def read_analog_soil_xbee_sensor(self,XbeeDevice:XBeeDevice,sensor_analog_pin):
        """
        This provides functionality for getting the sensor value on a Xbee Node

        Args:
            sensor_analog_pin (Integer) : The analog pin that sensor is connected to on XBee module 0=>DIO0,1->DIO1
            XbeeDevice (XBeeDevice) : The node device where the sensor is connected
        
        Returns:
            Sensor Value
        """
        sensor_value=0

        #Configure the  pin to analog (Pin must support Analog signal Pin 0-Pin3)!Uses pin 0 only now
       
        XbeeDevice.set_io_configuration(IOLine.DIO0_AD0,IOMode.ADC)
        sensor_value=XbeeDevice.get_adc_value(IOLine.DIO0_AD0)

        #Convert 10 Bit ADC value to percentage of water content in soil
        sensor_value=round(float(sensor_value/1023.0)*100,2) 

        #raise Exception('The selected pin does not support Analog');
        
        return str(sensor_value)
    
    def read_analog_temp_xbee_sensor(self,XbeeDevice:XBeeDevice,sensor_analog_pin):
        """
        This provides functionality for getting the sensor value on a Xbee Node

        Args:
            sensor_analog_pin (Integer) : The analog pin that sensor is connected to on XBee module 0=>DIO0,1->DIO1
            XbeeDevice (XBeeDevice) : The node device where the sensor is connected
        
        Returns:
            Sensor Value
        """
        sensor_value=0

        #Configure the  pin to analog (Pin must support Analog signal Pin 0-Pin3)!Uses pin 0 only now
       
        XbeeDevice.set_io_configuration(IOLine.DIO0_AD0,IOMode.ADC)
        sensor_value=XbeeDevice.get_adc_value(IOLine.DIO0_AD0)

        #Convert 10 Bit ADC value to percentage of water content in soil
        sensor_value=round(float(sensor_value/1023.0)*50,2) 

        #raise Exception('The selected pin does not support Analog');
        
        return str(sensor_value)

    
    def read_digital_xbee_sensor(self,xbee_device:XBeeDevice,io_digital_pin):
        """
        This function provides functionality for interfacing with the DHT11 Humidity and Temperature sensor 
        connected to an XBee 3 module

        Args:
            xbee_device (XBee Device): The Xbee module object that represents the XBee module 3 in the network
            io_digital_pin (Integer) : The digital IO pin that the sensor is connected to
        """
