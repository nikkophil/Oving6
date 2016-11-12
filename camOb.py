from basic_robot.camera import Camera
from basic_robot.imager2 import Imager

class CamOb:
    def __init__(self):
        # List of all associated sensors
        self.cam = Camera()
        self.sensor_list = [self.cam]
        self.value = None               #Imager() med bilde fra kamera
        self.skip = False

    def update(self):
        #oppdaterer kamera, og lagrer value som blir returnert
        if self.skip:
            return self.value
        self.value = Imager(image = self.cam.update())
        return self.value


    def get_value(self):
        #henter verdi fra cam, og lagrer den til self.value
        return self.value

    def reset(self):
        self.value = None
        self.cam.reset()


    # Add sensor to associated list
    def add_sensor(self, sensor):
        self.sensor_list.append(sensor)