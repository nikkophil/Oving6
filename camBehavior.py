from camOb import CamOb
from basic_robot.imager2 import Imager
from basic_robot.zumo_button import ZumoButton
from random import randint

class GetGoalColor:
    def __init__(self):
        print("Place ball infront and press button")
        ZumoButton().wait_for_press()

        img = CamOb().update()
        GoalColor = (0,0,0)
        xCenter = img.xmax//2
        yCenter = img.ymax//2

        for x in range(xCenter-5, xCenter+5):
            for y in range(yCenter-5, yCenter+5):
                GoalColor = img.combine_pixels(GoalColor, img.get_pixel(x,y))

        outStr = "True"
        for i in GoalColor:
            outStr += ", " + str(i)

        file = open("goalColor", mode='w')
        file.write(outStr)
        file.close()

class CamBehavior:
    #Husk, en behavior skal ikke kommunisere med en annen behavior!
    def __init__(self,bbcon,sensorList, priority):
        self.__bbcon = bbcon        #Pointer til kontrolleren, bruk til indirekte kommunikasjon
        self.__sensors = sensorList #Liste av sensor objektene som leverer info
        self.__motorRecs = [(0,"S", 0,False)]   #Anbefalinger som sendes til motorene, kan kanskje fernes og erstattes med en funskjon
        self.__active = True        #Bestemmer om behavior er aktiv
        self.__priority = priority  #Prioriteten til behavioren, tall mellom 0 og 1.
        self.__halt_request = False #Request å stoppe (avslutte bevegelse)
        self.__match_degree = 0     #Tall mellom 0 og 1 som indikerer hvor 'sikker' behavioren er på det den leser.
        self.__weight = 0           #Hvor 'viktig' anbefalingen er, =prioritet*match_degree
        self.__goalColor = []

        self.__timesCalled = 0
        file = open("goalColor")
        rgb = file.read().split(", ")
        file.close()
        learned = ('True' == rgb.pop(0))
        if learned:
            for x in rgb:
                self.__goalColor.append(int(x))

    #Obligatoriske funksjoner
    def consider_deactivation(self):
        seen = self.__motorRecs[0][1] == "F" or self.__motorRecs[0][2] == 10

        if self.__timesCalled == 1 and not seen:
            #print("Camera inactive!", self.__timesCalled)
            self.__active = False
            self.__bbcon.deactivate_behavior(self)
            self.__sensors[0].skip = True

    def consider_activation(self):
        #Whenever a behavior is inactive, it should test whether it should activate.
        if self.__timesCalled >= 3:
            #print("Camera active!", self.__timesCalled)
            self.__timesCalled = 0
            self.__active = True
            self.__bbcon.activate_behavior(self)
            self.__sensors[0].skip = False

    def update(self):
        #The main interface between the bbcon and the behavior (detailed below).
        #Test om behavioren skal aktiveres/deaktiveres:
        if (self.__active):
            self.consider_deactivation()
        else:
            self.consider_activation()
        #Hvis fortsatt aktiv, gjør dette:
        self.__timesCalled += 1
        if (self.__active):
            #print(">>>>>>>>>camera sensing!!!!!", self.__timesCalled)
            self.sense_and_act()
            self.__weight = self.__priority * self.__match_degree           #Oppdaterer weight, basert på data

    def sense_and_act(self):
        #The core computations performed by the behavior that use sensob readings to produce motor recommendations
        #  (and halt requests).
        #Husk å oppdatere match_degree
        #få Imager fra camOb
        img = self.__sensors[0].get_value()
        error = 0.15
        img_xmax = img.xmax
        img_ymax = img.ymax
        img_xmaxArea = img_xmax//3

        areas = ((0,img_xmaxArea),(img_xmaxArea+1, img_xmax-img_xmaxArea), (img_xmax-img_xmaxArea+1, img_xmax))
        bestArea = [10, -1]
        for i in range(len(areas)):
            area = areas[i]
            goalPixels = 0
            for x in range(area[0], area[1]):
                for y in range(img_ymax):
                    rgb = img.get_pixel(x,y)
                    r = (self.__goalColor[0]-self.__goalColor[0]*error < rgb[0] <= self.__goalColor[0]+self.__goalColor[0]*error)
                    g = (self.__goalColor[1]-self.__goalColor[1]*error < rgb[1] <= self.__goalColor[1]+self.__goalColor[1]*error)
                    b = (self.__goalColor[2]-self.__goalColor[2]*error < rgb[2] <= self.__goalColor[2]+self.__goalColor[2]*error)

                    if r and g and b:
                        goalPixels += 1

            if goalPixels > bestArea[0]:
                bestArea = [goalPixels, i]
        bestpart = bestArea[1]
        if bestpart != -1:
            self.__halt_request = False

            if bestpart == 1:
                print("[camBehavior]Considering halt:", bestArea[0], ">", 150)#img_xmaxArea*img_ymax*0.3)
                if bestArea[0] > 150: #img_xmaxArea*img_ymax*0.3:
                    print("[camBehavior]>------------ HALT ---------------<")
                    self.__halt_request = True

            self.__weight = self.__priority*0.6
            self.__match_degree = 0.6
            self.__motorRecs[0] = [(self.__weight, "L", 10, self.__halt_request),
                                (self.__weight, "F", 0.2, self.__halt_request),
                                (self.__weight, "R", 10, self.__halt_request)][bestpart]

        else:
            self.__halt_request = False
            self.__weight = self.__priority * 0.1
            self.__match_degree = 0.1
            self.__motorRecs[0] = [(self.__weight, "L", 45, self.__halt_request),(self.__weight, "R", 45, self.__halt_request)][randint(0,1)]

        #print("Cam concludes:", self.__motorRecs)

    def getRecs(self):
        #print("Cam returning:", self.__motorRecs)
        return self.__motorRecs

if __name__ == "__main__":
    GetGoalColor()