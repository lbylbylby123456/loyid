class Instruction:
    def __init__(self,MissingDataPoint,startDate,endDate,imo):
        self.__key = 'init'
        self.MissingDataPoint = MissingDataPoint
        self.startDate = startDate
        self.endDate = endDate
        self.imo = imo
    def get_key(self):
        return self.__key
    def set_key(self,key):
        self.__key=key

    def get_MissingDataPoint(self):
        return self.MissingDataPoint
    def set_MissingDataPoint(self, MissingDataPoint):
        self.MissingDataPoint = MissingDataPoint

    def get_startDate(self):
        return self.startDate
    def set_startDate(self, startDate):
        self.startDate = startDate

    def get_endDate(self):
        return self.endDate
    def set_endDate(self, endDate):
        self.endDate = endDate

    # def get_str(self):
    #     return self.__str
    # def set_str(self,str):
    #     self.__str=str

    def Instruction(self,imo):
        self.imo=imo


    def setParsingInterval(self):
        dates=self.get_MissingDataPoint()
        if(len(dates))>0:
            start_date=min(dates)
            end_date=max(dates)
            

