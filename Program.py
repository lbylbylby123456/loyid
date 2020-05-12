from datetime import datetime
import Instruction
import MySQLdb
import LloydsBrowserDriver
import MissingDataPoint
import sys
class Program(object):
    def __init__(self,MissingDates,PathMissingDates):
        self.__key = 'init'
    def get_key(self):
        return self.__key
    def set_key(self,key):
        self.__key=key
    #def DateTime(self):

    def get_MissingDates(self):
        return self.MissingDates

    def set_MissingDates(self,MissingDates):
        self.MissingDates=MissingDates

    MissingDates=property(get_MissingDates,set_MissingDates)

    def get_PathMissingDates(self):
        return self.PathMissingDates

    PathMissingDates=property(get_PathMissingDates)




    def parse(self,MissingDates,maxDaysBetweenDates):
        print("Parse pppp")
        #i=0
        imolist=[]
        for i in range (len(MissingDates)):
            imolist.append(MissingDates[i])
        shipNo=0
        #sys.path.append(r'C:\Users\lenovo\Desktop\teacher')

        while(shipNo<len(imolist)):
            print("Parse shipno:"+shipNo)

            imo=imolist[shipNo]
            #imolist = MissingDates
            missingDatapointList = MissingDates

            daysSinceLast = 0
            instruction = Instruction.Instruction()#???
            instruction.Instruction(imo)
            lastDataPoint = missingDatapointList.First()
            status = LloydsBrowserDriver.PageStatus.DataFound
            print("Parse 1")
            #foreach(dataPoint in missingDatapointList)
            for i in range(len(missingDatapointList)):
                dataPoint=missingDatapointList[i]
                if (status !=  LloydsBrowserDriver.PageStatus.ShipNonExistent):
                    daysSinceLast += 1

                    if (maxDaysBetweenDates >= daysSinceLast &&(dataPoint.Date.Date - lastDataPoint.Date.Date).TotalDays <= 1):
                        instruction.MissingDataPointCoveredByInstruction.append(dataPoint)
                    '''else:
                        instruction.SetParsingIntervall()
                        status = Proccess(instruction)

                        instruction = Instruction(imo)
                        instruction.MissingDataPointsCoveredByInstruction.append(dataPoint)
                        daysSinceLast = 0
                     '''
                else:
                    instruction.MissingDataPointCoveredByInstruction.append(dataPoint);

                lastDataPoint = dataPoint
            print("Parse 2")

            if (len(instruction.MissingDataPointsCoveredByInstruction())> 0):
                if (status !=  LloydsBrowserDriver.PageStatus.ShipNonExistent):
                    instruction.SetParsingIntervall()
                    status = self.Proccess(instruction)
                '''else:
                    UpdateMissingDatapointList(instruction, status)
                    WriteMissingDataPointList()
                    WriteLog(instruction, status)'''
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

    def Proccess(instruction):
        print("Process pppp")

        tableAndResult =driver.GetShipData(instruction)
        status = tableAndResult[1]
        dataTable = tableAndResult[0]

        #WriteLog(instruction, status);

        # if (status != PageStatus.Error)
        #     {
        #         UpdateMissingDatapointList(instruction, status);
        #     WriteMissingDataPointList();
        #     TransferAISDataToAzureSQL(dataTable);
        #     }

        return status


    #def WriteLog(self,instruction,result):

    #def  UpdateMissingDatapointList(self):

    # def WriteMissingDataPointList(self):
    #     print("WriteMissingDataPointList pppp")
    #     file.WriteLine("Imo\tMissingDate");
     #已经存在，可以不必写
    #def WriteMissingDataPointList(self):



    def GetMissingDataPointList(self,PathMissingDates):
        print("GetMissingDataPorintList pppp")
        file=PathMissingDates
        file.readline()
        while(file.readline()!=""):
            aDate=datetime.now
            fields = file.readline().split('\t')
            if fields[1].tostring():
                aDate=fields[1].tostring()
                aMissingDataPoint=MissingDataPoint.now#??
                imo=fields[0]
                Date=aDate
                self.MissingDates.append(aMissingDataPoint)



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
        if (len(dataTableAIS.rows)> 0):
            print("TransferAISDataToAzureSQL pppp---------------------------00000000000")
            con = MySQLdb.connection(Properties.Settings.Default.SQLConnection + ";Initial Catalog=" + "AISdb")
            con.Open()

            bulkCopy=SqlBulkCopy(con).now
            bulkCopy.BatchSize = 50000
            bulkCopy.DestinationTableName = "AIS_Data_Raw"

            bulkCopy.ColumnMappings.append("imo", "imo")
            bulkCopy.ColumnMappings.append("Date/Time", "[datetime]")
            bulkCopy.ColumnMappings.append("x", "longitude")
            bulkCopy.ColumnMappings.append("y", "latitude")
            bulkCopy.ColumnMappings.append("Destination", "destination")
            bulkCopy.ColumnMappings.append("Heading", "headingReported")
            bulkCopy.ColumnMappings.append("Speed over ground", "speed")
            bulkCopy.ColumnMappings.append("Course over ground", "heading")
            bulkCopy.ColumnMappings.append("Draught (m)", "draft")
            bulkCopy.ColumnMappings.append("Source Type", "source")
            bulkCopy.ColumnMappings.append("ETA", "eta")

            bulkCopy.ColumnMappings.append("Nearest Port", "nearestPort")
            bulkCopy.ColumnMappings.append("Distance (nm)", "distance")
            bulkCopy.BulkCopyTimeout = 60 * 60
            bulkCopy.WriteToServer(dataTableAIS)
            con.Close()


if __name__ == '__main__':
    driver=SetUpLloydsBrowserDriver(Properties.Settings.Default.username,Properties.Settings.Default.password)
    A=Program()
    A.GetMissingDataPointList()
