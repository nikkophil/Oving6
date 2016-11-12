from random import randint

class ProxyBehavior:
    #Husk, en behavior skal ikke kommunisere med en annen behavior!
    def __init__(self,bbcon,sensorList, priority):
        self.__bbcon = bbcon        #Pointer til kontrolleren, bruk til indirekte kommunikasjon
        self.__sensors = sensorList #Liste av sensor objektene som leverer info
        self.__motorRecs = []       #Anbefalinger som sendes til motorene, kan kanskje fernes og erstattes med en funskjon
        self.__active = True      #Bestemmer om behavior er aktiv
        self.__priority = priority  #Prioriteten til behavioren, tall mellom 0 og 1.
        self.__halt_request = False #Request å stoppe (avslutte bevegelse)
        self.__match_degree = 0     #Tall mellom 0 og 1 som indikerer hvor 'sikker' behavioren er på det den leser.
        self.__weight = 0           #Hvor 'viktig' anbefalingen er, =prioritet*match_degree
        self.__speed=0.2

    #Obligatoriske funksjoner
    def consider_deactivation(self):
        #Whenever a behavior is active, it should test whether it should deactivate.
        pass

    def consider_activation(self):
        #Whenever a behavior is inactive, it should test whether it should activate.
        pass

    def update(self):
        #The main interface between the bbcon and the behavior (detailed below).
        #Test om behavioren skal aktiveres/deaktiveres:
        if (self.__active):
            self.consider_deactivation()
        else:
            self.consider_activation()
        #Hvis fortsatt aktiv, gjør dette:
        if (self.__active):
            self.sense_and_act()

    def sense_and_act(self):
        #The core computations performed by the behavior that use sensob readings to produce motor recommendations
        #  (and halt requests).
        #Husk å oppdatere match_degree

        #self.sensors[0] = IR
        #self.sensors[1] = UltraSonic
        rightTrig, leftTrig = self.__sensors[0].get_value()
        frontTrig = self.__sensors[1].get_value()

        #Finn anbefaling
        #('F',0.5,False) <- standard speed
        #('R',45,False)
        rec = ('F',0,False)
        if leftTrig and frontTrig and rightTrig:
            self.__match_degree = 1
            rec = ('B', self.__speed, False)
        elif leftTrig and frontTrig:
            self.__match_degree = 1
            rec = ('F', self.__speed, False)
        elif frontTrig and leftTrig:
            self.__match_degree = 1
            rec  = ('L', 80, False)
        elif frontTrig and rightTrig:
            self.__match_degree = 1
            rec = ('R', 80, False)
        elif rightTrig:
            self.__match_degree = 0.7
            rec = ('R', 30, False)
        elif leftTrig:
            self.__match_degree = 0.7
            rec = ('L', 30, False)
        elif frontTrig:
            self.__match_degree = 1
            dir = randint(1, 2)
            if (dir == 1):
                rec = ('R', 80, False)
            else:
                #(dir == 2)
                rec = ('L', 80, False)

        else:
            self.__match_degree = 0.05
            rec = ('F', self.__speed, False)
        self.__weight = self.__priority*self.__match_degree

        recDir, recDeg, recStop = rec
        outRec = (self.__weight, recDir, recDeg, recStop)
        self.__motorRecs = [outRec]

    #Hjelpefunksjoner

    def getRecs(self):
        return self.__motorRecs
