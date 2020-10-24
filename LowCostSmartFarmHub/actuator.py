import time
from rpi_ws281x import Color, PixelStrip, ws

class Actuator:
    actuatorName:str
    actuatorID:int
    actuatorType:str
    actuatorValues:[]
    description:str
    def __init__(self,actuatorName,actuatorID,actuatorType,description,actuatorValues=None):
        self.actuatorName=actuatorName      #Every Actuator on the network has a name
        self.actuatorID=actuatorID          #Every Actuator on the network has a unique ID
        self.actuatorType=actuatorType      #DIO,DAC
        self.actuatorValues=actuatorValues  #[recent actuator commands]
        self.description=description        #More information about actuator ,humidity,Temperature

    def control_ws28x1_light(self,led_pin,state):
        """
        Function to  configure and control the ws28x1 RGB LED Strip
       
        Args:
	    led_pin:GPIO pin connected to the Pixels from RPI  (must Support PWM)
        Returns:
            current state of the light
        """
        # LED strip configuration:
        LED_COUNT = 32        # Number of LED pixels.
        LED_PIN = led_pin     # GPIO pin connected to the pixels (must support PWM!).
        LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA = 10           # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 10   # Set to 0 for darkest and 255 for brightest
        LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL = 0
        # LED_STRIP = ws.SK6812_STRIP_RGBW
        LED_STRIP = ws.SK6812W_STRIP
  
       # Create PixelStrip object with appropriate configuration.
        strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
        # Intialize the library (must be called once before other functions).
        strip.begin()
        if(state=="on"):
          strip.setPixelColor(0,Color(4,255,255))

        elif (state=="off"):
          strip.setPixelColor(0,Color(0,0,0))
        strip.show()
