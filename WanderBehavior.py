import random

class WanderBehavior():
    #Husk, en behavior skal ikke kommunisere med en annen behavior!
    def __init__(self,bbcon,sensorList, priority):
        self.__bbcon = bbcon        #Pointer til kontrolleren, bruk til indirekte kommunikasjon
        self.__sensors = sensorList #Liste av sensor objektene som leverer info
        self.__motorRecs = []       #Anbefalinger som sendes til motorene, kan kanskje fernes og erstattes med en funskjon
        self.__active = False       #Bestemmer om behavior er aktiv
        self.__priority = priority  #Prioriteten til behavioren, tall mellom 0 og 1.
        self.__halt_request = False #Request å stoppe (avslutte bevegelse)
        self.__match_degree = 0     #Tall mellom 0 og 1 som indikerer hvor 'sikker' behavioren er på det den leser.
        self.__weight = 0           #Hvor 'viktig' anbefalingen er, =prioritet*match_degree
        self.__speed = 0.5

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
            self.__weight = self.__priority * self.__match_degree           #Oppdaterer weight, basert på data

    def sense_and_act(self):
        #The core computations performed by the behavior that use sensob readings to produce motor recommendations
        #  (and halt requests).
        #Husk å oppdatere match_degree
        randDirection = random.randint(0,1)
        randAngle = random.randint(45,180)

        if randDirection == 0:
            self.__match_degree = 1
            self.__motorRecs= ["L", randAngle, False]
        elif randDirection == 1:
            self.__match_degree = 1
            self.__motorRecs = ["R", randAngle, False]

    #Hjelpefunksjoner

