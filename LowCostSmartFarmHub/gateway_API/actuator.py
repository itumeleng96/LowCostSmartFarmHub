class Actuator:
    actuatorName:str
    actuatorID:int
    actuatorType:str
    actuatorValues:[]
    description:str
    
    def __init__(self,actuatorName,actuatorID,actuatorType,actuatorValues,description):
        self.actuatorName=actuatorName      #Every Actuator on the network has a name
        self.actuatorID=actuatorID          #Every Actuator on the network has a unique ID
        self.actuatorType=actuatorType      #DIO,DAC
        self.actuatorValues=actuatorValues  #[recent actuator commands]
        self.description=description        #More information about actuator ,humidity,Temperature