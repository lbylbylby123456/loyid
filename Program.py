from datetime import datetime
from MySQLdb
class Program:
    def __init__(self):
        self.__key = 'init'
    def get_key(self):
        return self.__key
    def set_key(self,key):
        self.__key=key
    #def DateTime(self):


    def parse(self,maxDaysBetweenDates):
        print("Parse pppp")
        imolist=MissingDates
        shipNo=0

        while(shipNo<len(imolist)):
            print("Parse shipno:"+shipNo)

            imo=imolist[shipNo]
            imolist = MissingDates

            daysSinceLast = 0
            instruction = new Instruction(imo)
            lastDataPoint = missingDatapointList.First()
            status = PageStatus.DataFound
            print("Parse 1")
            foreach(dataPoint in missingDatapointList)
            if (status != PageStatus.ShipNonExistent):
                daysSinceLast += 1

                if (maxDaysBetweenDates >= daysSinceLast & &(dataPoint.Date.Date - lastDataPoint.Date.Date).TotalDays <= 1):
                    instruction.MissingDataPointsCoveredByInstruction.Add(dataPoint)

                else:
                    instruction.SetParsingIntervall()
                    status = Proccess(instruction)

                    instruction = new Instruction(imo)
                    instruction.MissingDataPointsCoveredByInstruction.Add(dataPoint)
                    daysSinceLast = 0
            else:
                instruction.MissingDataPointsCoveredByInstruction.Add(dataPoint);
            lastDataPoint = dataPoint
            print("Parse 2");

            if (len(instruction.MissingDataPointsCoveredByInstruction)> 0):
                if (status != PageStatus.ShipNonExistent)
                    instruction.SetParsingIntervall()
                    status = Proccess(instruction)
                else:
                    UpdateMissingDatapointList(instruction, status)
                    WriteMissingDataPointList()
                    WriteLog(instruction, status)
            shipNo += 1


            #Kill_Process("CHROMEDRIVER")
            #Kill_Process("CHROME")
            #driver = LloydsBrowserDriver.SetUpLloydsBrowserDriver\
            #(\
            #  Properties.Settings.Default.username,
            # Properties.Settings.Default.password
            #)
            #shipNo += 1

    #def Kill_Process(self,processName):

    #def Proccess(instruction):

    #def WriteLog(self,instruction,result):

    #def  UpdateMissingDatapointList(self):

    # def WriteMissingDataPointList(self):
    #     print("WriteMissingDataPointList pppp")
    #     file.WriteLine("Imo\tMissingDate");
     #已经存在，可以不必写
    #def WriteMissingDataPointList(self):



    def GetMissingDataPointList(self):
        print("GetMissingDataPorintList pppp")
        file=
        file.readline()
        while(file.readline()!=""):
            aDate=datetime.now
            fields = file.readline().split('\t')
            if fields[1].tostring():
                aMissingDataPoint
                imo=fields[0]
                Date=aDate
                MissingDates.add(aMissingDataPoint)



    '''def TransferAISDataToAzureSQL(self,dataTableAIS):
        print("TransferAISDataToAzureSQL pppp---------------------------[%d]"+len(dataTableAIS.Rows))
        n=len(dataTableAIS.Rows)
        if n>0 :
            print("TransferAISDataToAzureSQL pppp---------------------------00000000000")
            file1="content.txt"
            with open(file1,"a") as f:
                f.write()
    '''
    def TransferAISDataToAzureSQL(dataTableAIS):

        print("TransferAISDataToAzureSQL pppp---------------------------"+len(dataTableAIS.Rows))
        if (len(dataTableAIS.Rows)> 0):
            print("TransferAISDataToAzureSQL pppp---------------------------00000000000")
            con = MySQLdb.connection(Properties.Settings.Default.SQLConnection + ";Initial Catalog=" + "AISdb")
            con.Open()

            bulkCopy=SqlBulkCopy(con).now
            bulkCopy.BatchSize = 50000
            bulkCopy.DestinationTableName = "AIS_Data_Raw"

            bulkCopy.ColumnMappings.Add("imo", "imo")
            bulkCopy.ColumnMappings.Add("Date/Time", "[datetime]")
            bulkCopy.ColumnMappings.Add("x", "longitude")
            bulkCopy.ColumnMappings.Add("y", "latitude")
            bulkCopy.ColumnMappings.Add("Destination", "destination")
            bulkCopy.ColumnMappings.Add("Heading", "headingReported")
            bulkCopy.ColumnMappings.Add("Speed over ground", "speed")
            bulkCopy.ColumnMappings.Add("Course over ground", "heading")
            bulkCopy.ColumnMappings.Add("Draught (m)", "draft")
            bulkCopy.ColumnMappings.Add("Source Type", "source")
            bulkCopy.ColumnMappings.Add("ETA", "eta")

            bulkCopy.ColumnMappings.Add("Nearest Port", "nearestPort")
            bulkCopy.ColumnMappings.Add("Distance (nm)", "distance")
            bulkCopy.BulkCopyTimeout = 60 * 60
            bulkCopy.WriteToServer(dataTableAIS)
            con.Close()

    PathMissingDates= ""

if __name__ == '__main__':
    A=Program()
    A.GetMissingDataPointList()
