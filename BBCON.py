from time import sleep
from basic_robot.zumo_button import ZumoButton
from basic_robot.irproximity_sensor import IRProximitySensor
from basic_robot.ultrasonic import Ultrasonic
from IRProxySensOb import IRProxySensOB
from UltraSonicSensOb import UltraSonicSensOb
from edgeOb import EdgeOb
from motOb import MotOb
from Arbitrator import Arbitrator
from ProxyBehavior import ProxyBehavior
from camBehavior import CamBehavior
from WanderBehavior import WanderBehavior
from edgeBehavior import EdgeBehavior
from camOb import CamOb
from AngleTestBehavior import AngleTestBehavior

class BBCON:
    def __init__(self,sensObs,motObs):
        #Ha alle behaviors i active til all tid, legg behavior til inactive hvis den skal være inactiv
        self.__active_behaviors = []
        self.__inactive_behaviors = []
        self.__sensobs = sensObs
        self.__motobs = motObs
        self.__arbitrator = None
        self.__timeStepCount = 0

    def set_arbitrator(self,arbitrator):
        self.__arbitrator = arbitrator

    def add_behavior(self, behavior):
        behavior.__active = True
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
            self.__arbitrator.sendRecommendation(behavior.getRecs()[0])
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

    proxyPriority = 1
    linePriority = 0.8
    camPriority = 0.5
    wanderPriority = 0.2

    #Vent til knapp trykkes
    startButton = ZumoButton()
    startButton.wait_for_press()

    #Initialiserer objekter:

    #Sensor objekter:
    IrProxyOb = IRProxySensOB(IRProximitySensor())
    UltrasonicOb = UltraSonicSensOb(Ultrasonic())
    CameraOb = CamOb()
    EdgyOb = EdgeOb()
    sensObList = [IrProxyOb,UltrasonicOb,CameraOb,EdgyOb]

    #Motor objekter
    mainMotorOb = MotOb()
    motObList = [mainMotorOb]
    #BBCON
    brain = BBCON(sensObList,motObList)

    #Arbitrator objekt:
    MasterArbitrator = Arbitrator(brain)
    #Legg til brain
    brain.set_arbitrator(MasterArbitrator)

    #Behavior objekter:
    ProximityBehavior = ProxyBehavior(brain, [IrProxyOb,UltrasonicOb], proxyPriority)
    CameraBehavior = CamBehavior(brain,[CameraOb],camPriority)
    WanderingBehavior = WanderBehavior(brain,[],wanderPriority)
    EdgyBehavior = EdgeBehavior(brain,[EdgyOb],linePriority)
    AngleTester = AngleTestBehavior(brain, [], 1)
    #Legg til brain
    #brain.add_behavior(ProximityBehavior)
    #brain.add_behavior(CameraBehavior)
    brain.add_behavior(WanderingBehavior)
    #brain.add_behavior(EdgyBehavior)
    #brain.add_behavior(AngleTester)
    behaviorList = [ProximityBehavior, CameraBehavior, WanderingBehavior, EdgyBehavior]

    while True:
        brain.run_one_timestep()





if __name__ == '__main__': main()