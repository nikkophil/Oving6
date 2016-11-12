
class UltraSonicSensOb:
    def __init__(self,sensorWrapper):
        #Kun en sensor
        self.sensor = sensorWrapper
        self.distance = None

    def update(self):
        self.sensor.update()
        self.distance = self.sensor.get_value()
        return self.distance

    def get_value(self):
        #finner ut om noe er for nært
        if self.distance < 6:
            return True
        else:
            return False

    def reset(self,sensorWrapper):
        self.__init__(sensorWrapper)

    # Add sensor to associated list
    def add_sensor(self, sensor):
        self.sensor = sensor