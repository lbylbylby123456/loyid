class MissingDataPoint(object):
    def __init__(self,imo,date):
        self.__key = 'init'
        self.imo = imo
        self.date = date

    def get_imo(self):
        return self.imo
    def set_imo(self,imo):
        self.imo=imo

    def get_date(self):
        return self.date

    def set_date(self,date):
        self.date=date