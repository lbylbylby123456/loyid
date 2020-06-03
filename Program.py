from datetime import datetime
import time
import Instruction
import LloydsBrowserDriver
import MissingDataPoint
class Program():
    def __init__(self):
        self.__key = 'init'
        self.MissingDates = []
        #self.PathMissingDates='C:\\Users\\Eric\\Desktop\\Lloyds+Parser+Fill+Out+Missing+Data+3\\Lloyds Parser Fill Out Missing Data 3\\MissingRemainingData 3.txt'
        self.PathMissingDates = 'C:\\Users\\lenovo\Desktop\\Lloyds Parser Fill Out Missing Data 3\\Lloyds Parser Fill Out Missing Data\\MissingRemainingData 3.txt'

    def get_key(self):
        return self.__key
    def set_key(self,key):
        self.__key=key
    #def DateTime(self):

    def get_MissingDates(self):
        return self.MissingDates

    def set_MissingDates(self,MissingDates):
        self.MissingDates=MissingDates

    #MissingDates=property(get_MissingDates,set_MissingDates)

    def get_PathMissingDates(self):
        return self.PathMissingDates

    #PathMissingDates = property(get_PathMissingDates)
    driver = LloydsBrowserDriver.LloydsBrowserDriver()
    driver.SetUpLloydsBrowserDriver("liboyang@lll13.onexmail.com", "li123456")
    #老师请换成您自己的账号密码

    def parse(self, maxDaysBetweenDates):
        print("Parse pppp")

        ##!!!有问题这里！！！
        ##读取数据库
        imolist=[]
        for i in range(len(self.MissingDates)):
            imolist.append(self.MissingDates[i][0])
        shipNo=0

        while(shipNo<len(imolist)):
                print("Parse shipno:"+str(shipNo))

                imo=imolist[shipNo]
                #imolist = MissingDates
                missingDatapointList=[]

                def takeSecond(elem):
                    return elem[1]
                for i in range(len(self.MissingDates)):
                    if(self.MissingDates[i][0]==imo):
                        missingDatapointList.append(self.MissingDates[i])
                        #missingDatapointList.sort(key=takeSecond)

                print("missingDatapointList" + str(missingDatapointList[0]))
                daysSinceLast = 0
                instruction = Instruction.Instruction()
                instruction.Instruction(imo)
                lastDataPoint = missingDatapointList[0]
                status = LloydsBrowserDriver.PageStatus.DataFound.value
                print("Parse 1")

                #foreach(dataPoint in missingDatapointList)
                for i in range(len(missingDatapointList)):
                    print("missingDatapointList" + str(missingDatapointList[i][0]))
                    dataPoint = missingDatapointList[i]
                    if (status != LloydsBrowserDriver.PageStatus.ShipNonExistent.value):
                        daysSinceLast += 1
                        print("dataPoint[1]",dataPoint[1])
                        print("lastDataPoint[1]",lastDataPoint[1])
                        delta=dataPoint[1] - lastDataPoint[1]
                        interval = delta.days
                        print("detal:"+str(delta))
                        print("interval:" + str(interval))
                        #!!!!有错误
                        # x1=dataPoint[i].astype('timedelta64[D]').astype(int)
                        # y1=dataPoint[i].astype('timedelta64[h]').astype(int)
                        # x2=lastDataPoint[i].astype('timedelta64[D]').astype(int)
                        # y2=lastDataPoint[i].astype('timedelta64[h]').astype(int)
                        if (maxDaysBetweenDates >= daysSinceLast and abs(interval) <= 1):
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

                if (len(instruction.MissingDataPointCoveredByInstruction)> 0):
                    if (status !=  LloydsBrowserDriver.PageStatus.ShipNonExistent.value):
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

    #def Kill_Process(self,processName):#！！！没写

    def Proccess(self,instruction):
        print("Process pppp")
        tableAndResult = self.driver.GetShipData(instruction)
        status = tableAndResult[1]
        dataTable = tableAndResult[0]

        ##！！！datatable
        #WriteLog(instruction, status);

        #if (status != PageStatus.Error):
        if (status != LloydsBrowserDriver.PageStatus(4)):
            #self.UpdateMissingDatapointList(instruction, status)
            #self.WriteMissingDataPointList()
            self.TransferAISDataToAzureSQL(dataTable)

        return status


    #def WriteLog(self,instruction,result):

    def UpdateMissingDatapointList(self,instruction,status):
        print("UpdateMissingDatapointList pppp")
        if (status == LloydsBrowserDriver.PageStatus.ShipNonExistent.value):
            #决定一下有没有value！！
            for i in range(len(self.MissingDates)):
                print("MissingDates[i][0]" + self.MissingDates[i][0])
                if(self.MissingDates[i][0]==instruction.imo):
                    self.MissingDates.remove(self.MissingDates[i])

    def WriteMissingDataPointList(self):
        print("WriteMissingDataPointList pppp")
        file=open(self.PathMissingDates)
        file.writelines("Imo\tMissingDate")
        for i in range(len(self.MissingDates)):
            file.writelines(self.MissingDates[0]+"\t"+self.MissingDates[1])



    def GetMissingDataPointList(self):
        print("GetMissingDataPorintList pppp")
        file = open(self.PathMissingDates,'r')
        file.readline()
        fields = file.readline().split('\t')
        aDate = datetime.now
        while(fields!=""):
            if str(fields[1]):
                temp=[]
                #!!!AM
                #aDate=time.strptime(fields[1].replace(' AM\n',''), "%Y-%m-%d %H:%M:%S")
                aDate = datetime.strptime(fields[1].replace(' AM\n', ''), "%m/%d/%Y %H:%M:%S")
                #print(aDate)
                self.imo = fields[0]
                self.Date = aDate
                aMissingDataPoint=MissingDataPoint.MissingDataPoint(self.imo,self.Date)
                print(aMissingDataPoint)
                print(self.imo)
                print(self.Date)
                temp.append(self.imo)
                temp.append(self.Date)
                self.MissingDates.append(temp)
            fields = file.readline()
            if (not fields==''):
                fields=fields.split('\t')



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
    A=Program()
    A.GetMissingDataPointList()
    A.parse(14)
