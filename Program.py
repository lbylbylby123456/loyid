from datetime import datetime
import Instruction
import LloydsBrowserDriver
import MissingDataPoint
class Program():
    def __init__(self):
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

                    if (maxDaysBetweenDates >= daysSinceLast and (dataPoint.Date.Date - lastDataPoint.Date.Date).TotalDays <= 1):
                        instruction.MissingDataPointCoveredByInstruction.append(dataPoint)
                    '''else:
                        instruction.SetParsingIntervall()
                        status = Proccess(instruction)

                        instruction = Instruction(imo)
                        instruction.MissingDataPointsCoveredByInstruction.append(dataPoint)
                        daysSinceLast = 0
                     '''
                else:
                    instruction.MissingDataPointCoveredByInstruction.append(dataPoint)

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

    def Proccess(self,instruction):
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



    def GetMissingDataPointList(self):
        print("GetMissingDataPorintList pppp")
        file=self.PathMissingDates
        file.readline()
        while(file.readline()!=""):
            aDate=datetime.now
            fields = file.readline().split('\t')
            if fields[1].tostring():
                aDate=fields[1].tostring()
                aMissingDataPoint=MissingDataPoint.MissingDataPoint()#??
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

    '''def linesinsert(self, names, ages):
        try:
            # 连接数据库
            self.isConnectionOpen()
            # 创建游标
            global cursor
            cursor = self.__db.cursor()
            # sql命令
            sql = "insert into AIS_Data_Raw (name,age) value(%s,%s)"
            # 执行sql命令
            cursor.execute(sql, (names, ages))
        except Exception as e:
            print(e)
        finally:
            # 关闭游标
            cursor.close()
            # 提交
            self.__db.commit()
            # 关闭数据库连接
            self.__db.close()'''

    def TransferAISDataToAzureSQL(self,dataTableAIS):

        print("TransferAISDataToAzureSQL pppp---------------------------"+str(len(dataTableAIS.rows)))
        if (len(dataTableAIS.rows)> 0):
            print("TransferAISDataToAzureSQL pppp---------------------------00000000000")
            file1 = "content.txt"
            with open(file1, "w") as f:
                f.write("")
                f.close()
            with open(file1, "a") as f:
                f.write("imo  Date/Time  x  y  Destination  Heading  Speed over ground  Course over ground  Draught (m)  Source Type  ETA  Nearest Port  Distance (nm)\n")
                for i in range (len(dataTableAIS.rows)):
                    f.write(str(dataTableAIS.rows[i][0]))
                    f.write(str(dataTableAIS.rows[i][1]))
                    f.write(str(dataTableAIS.rows[i][2]))
                    f.write(str(dataTableAIS.rows[i][3]))
                    f.write(str(dataTableAIS.rows[i][4]))
                    f.write(str(dataTableAIS.rows[i][5]))
                    f.write(str(dataTableAIS.rows[i][6]))
                    f.write(str(dataTableAIS.rows[i][7]))
                    f.write(str(dataTableAIS.rows[i][8]))
                    f.write(str(dataTableAIS.rows[i][9]))
                    f.write(str(dataTableAIS.rows[i][10]))
                    f.write(str(dataTableAIS.rows[i][11]))
                    f.write(str(dataTableAIS.rows[i][12]+"\n"))

                f.close()




            '''
            con = MySQLdb.connection("localhost","AISdb","sa","4Fv*zBr984.xhz@!tYbQU4H-")
            con.open()

            bulkCopy=SqlBulkCopy(con)
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
            '''


if __name__ == '__main__':
    #driver=SetUpLloydsBrowserDriver(Properties.Settings.Default.username,Properties.Settings.Default.password)
    driver=LloydsBrowserDriver.LloydsBrowserDriver().SetUpLloydsBrowserDriver("sa","4Fv*zBr984.xhz@!tYbQU4H-")
    A=Program()
    A.GetMissingDataPointList()
