
class EdgeBehavior:
    #Husk, en behavior skal ikke kommunisere med en annen behavior!
    def __init__(self,bbcon,sensorList, priority):
        self.__bbcon = bbcon        #Pointer til kontrolleren, bruk til indirekte kommunikasjon
        self.__sensors = sensorList #Liste av sensor objektene som leverer info
        self.__motorRecs = []       #Anbefalinger som sendes til motorene, kan kanskje fernes og erstattes med en funskjon
        self.__active = True        #Bestemmer om behavior er aktiv
        self.__priority = priority  #Prioriteten til behavioren, tall mellom 0 og 1.
        self.__halt_request = False #Request å stoppe (avslutte bevegelse)
        self.__match_degree = 0     #Tall mellom 0 og 1 som indikerer hvor 'sikker' behavioren er på det den leser.
        self.__weight = 0           #Hvor 'viktig' anbefalingen er, =prioritet*match_degree
        self.__speed = 0.2
        self.sensor = sensorList[0]
        self.reflectanceValue = 0.1


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
        self.__motorRecs = []
        self.reflectances = self.sensor.get_value()
        print("Refelctances ", self.reflectances)
        #Verdien av de tre sensorene til henoldsvis høyre og venstre
        if self.edge():
            self.__match_degree = 1
            self.__weight = self.__priority * self.__match_degree
            #Sjekker om den treffer en linje fra høyre eller venstre side
            if self.reflectances[5] < self.reflectances[0]:
                recs = (self.__weight, 'L', 130, False)
            elif self.reflectances[0] < self.reflectances[5]:
                recs = (self.__weight, 'R', 130, False)
            else:
                recs = (self.__weight,'B', self.__speed, False)
        else:
            self.__match_degree = 0.1
            self.__weight = self.__priority * self.__match_degree
            recs = (self.__weight, 'F', self.__speed, False)

        self.__motorRecs.append(recs)

    #Hjelpefunksjon
    #Sjekker om signalet er sterk nok
    def edge(self):
        for i in self.reflectances:
            if i < self.reflectanceValue:
                return True
        return False

    def getRecs(self):
        return self.__motorRecs




