from basic_robot.reflectance_sensors import ReflectanceSensors

class EdgeOb():

    def __init__(self):
        # List of all associated sensors
        self.sensor = ReflectanceSensors()


    def update(self):
        return self.sensor.update()


    def get_value(self):
        self.reflectance = self.sensor.get_value()
        return self.reflectance

    def reset(self):
        self.sensor.reset()


    # Add sensor to associated list
    def add_sensor(self, sensor):
        self.sensor_list.append(sensor)