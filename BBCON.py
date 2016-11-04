from time import sleep
from basic_robot.zumo_button import ZumoButton

class BBCON:
    def __init__(self,behaviors,sensObs,motObs,arbitrator):
        #Ha alle behaviors i active til all tid, legg behavior til inactive hvis den skal være inactiv
        self.__active_behaviors = behaviors
        self.__inactive_behaviors = []
        self.__sensobs = sensObs
        self.__motobs = motObs
        self.__arbitrator = arbitrator
        self.__timeStepCount = 0

    def add_behavior(self, behavior):
        self.__active_behaviors.append(behavior)

    def add_sensob(self,sensOb):
        self.__sensobs.append(sensOb)

    def activate_behavior(self, behavior):
        if behavior in self.__inactive_behaviors:
            self.__inactive_behaviors.remove(behavior)

    def deactivate_behavior(self,behavior):
        if behavior not in self.__inactive_behaviors:
            self.__inactive_behaviors.append(behavior)

    def run_one_timestep(self):
        #Update sensObs:
        for sensor in self.__sensobs:
            sensor.update()
        #Update behaviors:
        for behavior in self.__active_behaviors:
            behavior.update()
        #Get info from arbitrator stop/update motObs
        rec = self.__arbitrator.choose_action()
        if rec[3]:
            #Usikker på om dette er alt som skal gjøres, må sikkert fikses senere
            for behavior in self.__active_behaviors:
                self.deactivate_behavior(behavior)
        for motOb in self.__motobs:
            rec = (rec[1],rec[2])
            motOb.update(rec)
        #Sleep, i sekunder
        sleep(0.5)
        #Reset sensors?



def main():
    startButton = ZumoButton()
    startButton.wait_for_press()



if __name__ == '__main__': main()