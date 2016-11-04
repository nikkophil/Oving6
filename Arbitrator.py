from random import random

class Arbitrator:
    def __init__(self,BBCON):
        self.__bbcon = BBCON
        self.__recList = []

    def sendRecommendation(self, recTuple):
        self.__recList.append(recTuple)

    def choose_action(self):
        weightRange = [0]
        for recTuple in self.__recList:
            weight, direction, degree, stop = recTuple
            weightRange.append(weight+weightRange[-1])

        probRange = weightRange[-1]*random()

        recNum = 0
        for i in range(len(weightRange)-1):
            if probRange < weightRange[i]:
                recNum = i-1
                break

        outRec = self.__recList[recNum]
        self.__recList=[]
        return outRec



