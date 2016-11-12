from basic_robot.motors import Motors
import math

class MotOb:
    def __init__(self):
        self.operations = {'L': self.__turn_left,
                           'R': self.__turn_right,
                           'F': self.__move_forwards,
                           'B': self.__move_backwards,
                           'S': self.stop}

        self.fullRotTid = 1.5
        self.motors = Motors()
        self.value = None

    # Saves MR, and runs it
    # MR must be list with (operation, setting)
    def update(self, MR):
        self.value = MR
        self.operationalize()

    def operationalize(self):
        self.operations[self.value[0]]()

    #TODO
    def __turn_left(self):
        #At a speed of 0.5(of max), it takes about 3 seconds to rotate 360 degrees
        angle = self.value[1]
        speed = 0.5


        turnTime = self.fullRotTid*angle/360
        #print("left:", angle, turnTime)

        self.motors.set_value([-speed,speed], turnTime)

    #TODO
    def __turn_right(self):
        angle = self.value[1]
        speed = 0.5

        turnTime = self.fullRotTid * angle / 360

        #print("left:", angle, turnTime)

        self.motors.set_value([speed, -speed], turnTime)

    def __move_backwards(self):
        speed = self.value[1]
        self.motors.backward(speed)

    def __move_forwards(self):
        speed = self.value[1]
        self.motors.forward(speed)

    def stop(self):
        self.motors.stop()
