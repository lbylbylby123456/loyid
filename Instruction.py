class Instruction(object):
    # def __init__(self,MissingDataPointCoveredByInstruction,startDate,endDate,imo):
    #     self.__key = 'init'
    #     self.MissingDataPoint = MissingDataPointCoveredByInstruction
    #     self.startDate = startDate
    #     self.endDate = endDate
    #     self.imo = imo
    def __init__(self):
        self.__key = 'init'
    def get_key(self):
        return self.__key
    def set_key(self,key):
        self.__key=key

    def get_MissingDataPointCoveredByInstruction(self):
        return self.MissingDataPointCoveredByInstruction
    def set_MissingDataPointCoveredByInstruction(self, MissingDataPointCoveredByInstruction):
        self.MissingDataPointCoveredByInstruction = MissingDataPointCoveredByInstruction

    MissingDataPointsCoveredByInstruction=property(get_MissingDataPointCoveredByInstruction,set_MissingDataPointCoveredByInstruction)

    def get_startDate(self):
        return self.startDate
    def set_startDate(self, startDate):
        self.startDate = startDate

    startDate=property(get_startDate,set_startDate)

    def get_endDate(self):
        return self.endDate
    def set_endDate(self, endDate):
        self.endDate = endDate

    endDate=property(get_endDate,set_endDate)

    def get_imo(self):
        return self.imo
    def set_imo(self,imo):
        self.imo=imo

    imo=property(get_imo,set_imo)

    def Instruction(self,imo):
        self.imo=imo


    def SetParsingIntervall(self):
        priPoint=self.get_MissingDataPointCoveredByInstruction()
        dates=[]
        for i in range(len(priPoint)):
            if(priPoint[i].Date):
                dates.append(priPoint[i])
        if(len(dates))>0:
            startDate=min(dates)
            endDate=max(dates)
            

