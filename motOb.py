from basic_robot.motors import Motors
import math

class MotOb:


    def Read_Zumo_Volts_AREF(self):
        return 1

    def __calc_turn_length(self, speed):
        y = 3.3375e-6*speed**3 - 0.00327*speed*speed + 1.0536*speed - 28.595
        length = 10.0*90.0/y
        return length

    def __calc_time(self, speed, length):
        a = 24069*speed**(-1.238)
        b = 5.7824*math.log(speed) - 19.99
        time = length * a + b
        correction = None
        if speed > 100:
            correction = -0.0007 * speed + 1.154

        elif speed > 50:
            correction = 0.0017 * speed + 0.9167

        else:
            correction = 0.0187 * speed + 0.0667

        time = time/correction
        #battery_volt =self.Read_Zumo_Volts_AREF()
        #time = time * 5.2 /battery_volt
        return time


    def __init__(self):
        self.operations = {'L': self.__turn_left,
                           'R': self.__turn_right,
                           'F': self.__move_forwards,
                           'B': self.__move_backwards,
                           'S': self.stop}

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
        angle = self.value[1]
        speed = self.motors.max*0.25
        self.stop()

        length = self.__calc_turn_length(speed)
        length = length*angle/90.0

        time = self.__calc_time(speed, length)
        speed = 0.25

        self.motors.set_value([-speed,speed], time)

    #TODO
    def __turn_right(self):
        angle = self.value[1]
        speed = self.motors.max * 0.25
        self.stop()

        length = self.__calc_turn_length(speed)
        length = length * angle / 90.0

        time = self.__calc_time(speed, length)
        speed = 0.25

        self.motors.set_value([speed, -speed], time)

    def __move_backwards(self):
        speed = self.value[1]
        self.motors.backward(speed)

    def __move_forwards(self):
        speed = self.value[1]
        self.motors.forward(speed)

    def stop(self):
        self.motors.stop()
