class MissingDataPoint():
    def __init__(self):
        self.__key = 'init'

    def get_imo(self):
        return self.imo
    def set_imo(self,imo):
        self.imo=imo

    imo=property(get_imo,set_imo)

    def get_date(self):
        return self.date

    def set_date(self,date):
        self.date=date

    date = property(get_date, set_date)