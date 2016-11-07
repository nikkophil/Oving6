
class IRProxySensOB:
    def __init__(self,sensorWrapper):
        #One sensor wrapper to rule them all (begge proxy sensorene)
        self.sensor = sensorWrapper
        self.rightTrig = False
        self.leftTrig = False

    def update(self):
        self.rightTrig, self.leftTrig = self.sensor.update()
        return self.rightTrig, self.leftTrig

    def get_value(self):
        return self.rightTrig, self.leftTrig

    def reset(self,sensorWrapper):
        self.__init__(sensorWrapper)

    # Ingen liste, sensor erstattes
    def add_sensor(self, sensor):
        self.sensor = sensor