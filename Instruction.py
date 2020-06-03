class Instruction(object):
    def __init__(self):
        self.__key = 'init'
        self.MissingDataPointCoveredByInstruction =[]
        self.startDate = None
        self.endDate = None
        self.imo = None


    def get_key(self):
        return self.__key
    def set_key(self,key):
        self.__key=key

    def get_MissingDataPointCoveredByInstruction(self):
        return self.MissingDataPointCoveredByInstruction
    def set_MissingDataPointCoveredByInstruction(self, MissingDataPointCoveredByInstruction):
        self.MissingDataPointCoveredByInstruction = MissingDataPointCoveredByInstruction

    #MissingDataPointsCoveredByInstruction=property(get_MissingDataPointCoveredByInstruction,set_MissingDataPointCoveredByInstruction)

    def get_startDate(self):
        return self.startDate
    def set_startDate(self, startDate):
        self.startDate = startDate

    #startDate=property(get_startDate,set_startDate)

    def get_endDate(self):
        return self.endDate

    def set_endDate(self, endDate):
        self.endDate = endDate

    #endDate=property(get_endDate,set_endDate)

    def get_imo(self):
        return self.imo

    def set_imo(self,imo):
        self.imo=imo

    #imo=property(get_imo,set_imo)

    def Instruction(self,imo):
        self.imo=imo


    def SetParsingIntervall(self):
        priPoint=self.get_MissingDataPointCoveredByInstruction()
        dates=[]
        for i in range(len(priPoint)):
            print("priPoint[i][1]:"+str(priPoint[i][1]))
            if(priPoint[i][1]):
                dates.append(priPoint[i][1])
        if(len(dates))>0:
            self.startDate=min(dates)
            #print("self.startDate:"+self.startDate)
            self.endDate=max(dates)
            #print("self.endDate:" + self.endDate)

