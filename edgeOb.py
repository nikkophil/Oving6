from basic_robot.reflectance_sensors import ReflectanceSensor

class EdgeOb():


    # test av oppdatering
    def __init__(self):
        # List of all associated sensors
        self.sensor = ReflectanceSensor()


    def update(self):
        self.sensor.Update()


    def get_value(self):
        self.reflectance = self.sensor.get_value()
        return self.reflectance

    def reset(self):
        self.sensor.reset()


    # Add sensor to associated list
    def add_sensor(self, sensor):
        self.sensor_list.append(sensor)