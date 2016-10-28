class Sensobs():

    def __init__(self):
        # List of all associated sensors
        sensor_list = []

    def update(self):
        raise NotImplementedError

    def get_value(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError


    # Add sensor to associated list
    def add_sensor(self, sensor):
        self.sensor_list.append(sensor)