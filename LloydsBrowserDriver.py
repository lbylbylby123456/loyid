#import OpenQA
import argparse
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from enum import Enum
import time
from ChromeOptions import ChromeOptions
#from DataTable import DataTable
from pandas import pandas
import numpy as np
import urllib.request
import requests
from datetime import datetime,timedelta
import click
import random
import select
class PageStatus(Enum):
    ShipNonExistent=1
    NoDataFound=2
    SuccessfulOperation=3
    DataFound=4
    Error=5

class LloydsBrowserDriver(ChromeDriver):
#class LloydsBrowserDriver():
    lloydsWebSite="https://www.lloydslistintelligence.com/"
    #wait
    driver = webdriver.Chrome()
    def get_password(self):
        return self.password
    def set_password(self,password):
        self.password=password

    def get_username(self):
        return self.username
    def set_username(self,username):
        self.username=username

    def get_PageStatus(self):
        return self.PageStatus

    def set_PageStatus(self,PageStatus):
        self.PageStatus =PageStatus

    def LloydsBrowserDriver(self,username,password):
        time.sleep(30)#???
        self.username=username
        self.password = password

    def SetUpLloydsBrowserDriver(self,username,password):
        print("SetUpLloydsBrowserDriver zzzz")

        c_service = Service('xxx')
        c_service.command_line_args()
        c_service.start()
        #driver = webdriver.Chrome()
        driver.get("http://www.baidu.com")

        #chromeServices = ChromeDriverService.CreateDefaultService()
        chromeServices = Service.CreateDefaultService()
        chromeServices.HideCommandPromptWindow = True
        chromeServices.SuppressInitialDiagnosticInformation = True

        opt = ChromeOptions() #浏览器选项??
        parser = argparse.ArgumentParser()
        parser.add_argument("--user-data-dir=c:\\Historical Parser")
        parser.add_argument("--dns-prefetch-disable")
        parser.add_argument("start-maximized")
        parser.add_argument("disable-infobars")
        parser.add_userProfilePreference("safebrowsing.enabled", True)
        return LloydsBrowserDriver(chromeServices, opt, username, password)


    def GetShipData(self,instruction):
        print("GetShipData zzzz")
        imoNo = instruction.imo.ToString()

        self.PageStatus = LloydsBrowserDriver.GoToShipMovements(instruction)
        table = pandas.DataFrame()

        if (self.PageStatus == PageStatus.SuccessfulOperation):
            table = self.FillDataTable(instruction)
            self.CleanAISData(table, instruction)
        return (table, self.PageStatus)

    def GoToShipMovements(self,instruction):

        print("GoToShipMovements zzz")
        result = PageStatus.SuccessfulOperation
        imoNo = instruction.imo.ToString()
        time.sleep(2)
        Url=requests.get(self.lloydsWebSite)
        if (Url in {"https://www.lloydslistintelligence.com/","https://www.lloydslistintelligence.com"}):
            time.sleep(0.5)
            result = self.GoToShipPageFromMainPage(imoNo)
            print("GoToShipPageFromMainPage")
        elif (not("?term" in Url) and ("vessel" in Url) and ("overview" in Url or "movements" in Url)):
            time.sleep(0.5)
            result = self.GoToShipFromShipPage(imoNo)
            print("GoToShipFromShipPage")
        else:
            print("else")
            time.sleep(0.5)
            self.GoToLloydsMainPage()
            self.Login()
            result = self.GoToShipPageFromMainPage(imoNo)
        if (result == PageStatus.SuccessfulOperation):
            print("GoToShipMovements zzzz PageStatus.SuccessfulOperation")
            self.WaitFindElementByTagAndText("a", "Vessels", 0, 2, 2)
            if ("term" in Url):
                time.sleep(0.5)
                result = self.GoToShipFromTermPage(imoNo)
                print("GoToShipFromTermPage")
            time.sleep(0.5)
            print("GoToAISDataPageFromShipPage")
            if (self.CheckIfCorrectShipPage(imoNo)):
                result = self.GoToAISDataPageFromShipPage()
            else:
                return PageStatus.Error
        print("GoToShipMovements zzzz PageStatus.error")
        return result

    # 需要Python3

    # def foreach(function, iterator):
    #     for item in iterator:
    #         function(item)

    def SetHeaders(self,table):
        print("SetHeaders zzz")
        table.Columns.Add("imo", type=int)
        table.Columns.Add("Current Position", type=str)
        table.Columns.Add("x", type=object)
        table.Columns.Add("y", type=object)
        table.Columns.Add("ETA", type=object)
        #headers = FindElementsByTagName("th").Select(x= > x.Text).ToList()
        driver= webdriver.Chrome(executable_path="chromedriver.exe")
        priheaders = driver.find_element_by_tag_name("th")
        headers = []
        for i in range(len(priheaders)):
            if (priheaders[i].Date):
                headers.append(priheaders[i])

        for i in range (len(headers)):
            header=headers[i]
        #foreach(header,headers):
            table.Columns.Add(header)

    def FillDataTable(self,instruction):
        print("FileDataTable zzzz")
        tableData = pandas.DataFrame()
        #driver = webdriver.Chrome()
        self.SetHeaders(tableData)
        date = datetime.utcnow
        self.ChangeFromToDate(instruction.startDate, instruction.endDate)
        self.AddAISDataToTable(tableData, instruction)
        isDataTransferred = False
        isDateChanged = False
        attempts = 2
        PageSource = self.driver.get('http://culture.dzwww.com/wx/')
        checkIfNoDataTextInTable = ("There is no data to display." in PageSource)
        if checkIfNoDataTextInTable:
                self.PageStatus = PageStatus.NoDataFound
        return tableData

    def ChangeFromToDate(self,fromDate, toDate):
        print("ChageFromToDate zzzz")
        dateElements = self.FindElementsByClassName("react-datepicker-wrapper")
        fromDateBox = dateElements[0].FindElement(By.TAG_NAME("input"))
        toDateBox = dateElements[1].FindElement(By.TAG_NAME("input"))
        fromDate=str(fromDate)
        toDate = str(toDate)


        fromDateBox.Click()
        fromDateBox.Clear()
        time.sleep(0.5)
        #fromDateBox.SendKeys(str(np.repeat(Keys.Backspace.ToString(),22)))
        fromDateBox.send_keys(str(np.repeat(str(Keys.BACKSPACE),22)))
        fromDateBox.SendKeys(time.strptime(fromDate,"%d/%m/%y").replace(".", "/") + "\n\r\n")
        time.sleep(0.5)
        dateElements[0].Click()
        time.sleep(0.5)

        toDateBox.Click()
        toDateBox.Clear()
        time.sleep(0.5)

        #toDateBox.SendKeys(string(Concat(Enumerable.Repeat(Keys.Backspace.ToString(), 22))))
        toDateBox.SendKeys(str(np.repeat(str(Keys.BACKSPACE),22)))
        time.sleep(0.5)
        toDateBox.SendKeys(time.strptime(fromDate,"%d/%m/%y").replace(".", "/") + "\n\r\n")
        time.sleep(0.5)
        dateElements[1].Click()

        #wait.Timeout = TimeSpan(0, 0, 20)
        #wait.Until(x= > !PageSource.Contains("Loading data"))
        #wait.Timeout = new TimeSpan(0, 0, 30)

        #wait=timedelta(seconds=20)
        time.sleep(20)
        while("Loading data" in PageSource):
            x=1
        time.sleep(20)
        #wait=timedelta(seconds=20)

    def GetPageCurrentPage(self):

        print("GetPageCurrentPage zzzz")
        #pageNo = (int)Parse(self.FindElementByClassName("lli-grid-pager__input").GetAttribute("value"))
        pageNo = int(self.driver.find_element(By.CLASS_NAME,"lli-grid-pager__input").get_attribute("value"))
        return pageNo

    def GoToNextPage(self):
        print("GoToNextPage zzzz")
        currentPageNo = self.GetPageCurrentPage()
        self.ClickNextPage()
        newPageNo = self.GetPageCurrentPage()
        return newPageNo > currentPageNo

    def  ClickNextPage(self):
        print("ClickNextPage zzzz")
        disclaimerBanners = self.driver.find_elements(By.CLASS_NAME("flaticon-cross"))
        if (len(disclaimerBanners)!= 0):
            disclaimerBanners.First().Click()
        buttons = self.driver.find_element(By.CLASS_NAME("lli-grid-pager__link--next"))
        if (not("disabled" in buttons.get_attribute("class"))):
            buttons.Click()

    def AddAISDataToTable(self,dataTable,instruction):
        print("AddAISDataToTable zzzz")
        time.sleep(2)
        #wait.Timeout = new TimeSpan(0, 0, 1)
        time.sleep(1)
        #PageSource.Contains("loading data")
        #wait.Timeout = new TimeSpan(0, 0, 30)
        time.sleep(30)
        tableString = self.driver.find_element(By.TAG_NAME,"table").get_attribute("innerHTML")
        #htmlDoc = HtmlAgilityPack.HtmlDocument()

        if (not("There is no data to display."in tableString)):
            #htmlDoc.LoadHtml(tableString)
            #table = htmlDoc.DocumentNode.Descendants("tr").Select(x => x.Descendants("td").Select(y => y.InnerText).ToList()).ToList()
            ##删掉了select
            headers = list(self.driver.find_elements(By.TAG_NAME,"th"))
            table = table.Where(x => x.Count > 0).ToList()
            #foreach (row in table):
            for i in range(len(table)):
                row=table[i]
                print("foreach row ------------")
                date = datetime.now
                if ("Date/Time" in headers and len(row) > 6):
                    print("foreach row -----in-------{0}",str(row[headers.IndexOf("Date/Time")]))

                    # if (float.TryParse(numberAsString.strip(), out fl))
                    #if (isinstance(numberAsString.strip(), float)):
                    #if (DateTime.TryParse(row[headers.IndexOf("Date/Time")].ToString(), out date)):
                    if (isinstance(str(row[headers.IndexOf("Date/Time")]),date)):#??
                    newRow = dataTable.NewRow()
                    print("foreach     colum --------row.count-{0:g}", row.Count)
                    for (int columnNo = 0; columnNo < row.Count; columnNo++):
                    columnName = headers[columnNo];
                    print("foreach     colum ----------lll--{0:g}, {0:g}", columnNo, row.Count)
                    if (row.Count > columnNo):
                    print("foreach     colum ------------  nooooooooooo");
                    newRow[columnName] = row[columnNo]
                    dataTable.Rows.Add(newRow)
                    else
                            print("AddAISDataToTable llll When adding data the row was found to be to short.");
                        print("When adding data the row was found to be to short.")

    def GoToShipFromTermPage(self,imoNo):
        print("GoToShipFromTermPage zzzz")
        self.WaitFindElementByTagAndText("a", "Vessels", 0, 2, 2)
        #tableRows = FindElementsByTagName("tr")
        tableRows = self.driver.find_elements(By.TAG_NAME,"tr")
        #foreach(row in tableRows):
        for i in range(len(tableRows)):
            row=tableRows[i]
            columnsWithImo = row.find_elements(By.TAG_NAME("td")).Where(x= > x.Text == imoNo).ToList()
        if (len(columnsWithImo) > 0):
           row.FindElements(By.TAG_NAME,"a").Where(x = > x.GetAttribute("href").Contains("vessel")).First().Click()
           return PageStatus.SuccessfulOperation
        return PageStatus.ShipNonExistent

    def GoToShipFromShipPage(self,imoNo):
        print("GoToShipFromShipPage zzzz")
        self.driver.find_element(By.CLASS_NAME,"lli-searchform__input").Click()
        self.driver.find_element(By.CLASS_NAME,"lli-searchform__input").SendKeys(string.Join("",\
            Enumerable.Repeat(Keys.Backspace.ToString(), 15 + (new Random()).Next(10))))
        self.driver.find_element(By.CLASS_NAME,"lli-searchform__input").SendKeys(imoNo)

        time.sleep(0.5 + random.uniform(0,2))
        self.driver.find_element(By.CLASS_NAME,"lli-searchform__button").Click()
        return PageStatus.SuccessfulOperation


    def ParseLongitudeAndLatitude(self,longOrLat):
        print("SetUpLloydsBrowserDriver zzzz")
        #splittedString =longOrLat.Split({ "N", "S" }, StringSplitOptions.RemoveEmptyEntries)
        splittedString = longOrLat.Split({"N", "S"}, StringSplitOptions.RemoveEmptyEntries)
        if(len(splittedString)>2):
            latitudeString = splittedString[0]
            longitudeString = splittedString[1]

            isSouth = longOrLat.Contains("S")
            isWest = longOrLat.Contains("W")

            y = ConvertToDecimalDegrees(latitudeString, isSouth)
            x = ConvertToDecimalDegrees(longitudeString, isWest)
            return (x,y)
        else:
            return (None, None)

    def GoToAISDataPageFromShipPage(self):
        print("GoToAISDataPageFromShipPage zzzz")
        self.WaitFindElementByTagAndText("a", "Movements", 0, 5, 5)
        self.driver.FindElements(By.TAG_NAME("a")).Where(x => x.Text == "Movements").First().Click()
        print("GoToAISDataPageFromShipPage zzzz Movements clicked")
        self.WaitFindElementByTagAndText("h1", "Ports and Passings", 0, 5, 5)

        self.driver.find_element(By.TAG_NAME("button").Where(x => x.Text == "AIS Positions").First().Click()
        print("GoToAISDataPageFromShipPage zzzz AIS Positions clicked")
        self.WaitFindElementByTagAndText("h1", "AIS Positions", 0, 5, 5)
        print("GoToAISDataPageFromShipPage zzzz AIS Positions finished")
        return PageStatus.SuccessfulOperation

    def CheckIfCorrectShipPage(self,imoNo):
        print("CheckIfCorrentShipPage zzzz")
        while(len(self.FindElementsByClassName("lli-infobar"))> 0):
            x=1
        imoInInfo = self.driver.find_element(By.CLASS_NAME,"lli-infobar").find_elements(By.TAG_NAME,("div"))[2].Text
        imo = string.Join("", imoInInfo.Where(x= > char.IsNumber(x)))
        return imoNo == imo

    def GoToShipPageFromMainPage(self,imoNo):
            print("GoToShipPageFromMainPage zzzz")
            time.sleep(2)
            if (Url.Contains("signin")):
                self.Login()
                return GoToShipPageFromMainPage(imoNo)
            else:
                Navigate().GoToUrl("https://www.lloydslistintelligence.com/vessels/")
                time.sleep(0.5+random.uniform(0,1))
                if (Url.Contains("signin")):
                    self.Login()

                time.sleep(random.random(1))#???
                self.driver.find_element(By.CLASS_NAME,"lli-searchform__input").SendKeys(imoNo)
                self.driver.find_element(By.CLASS_NAME,"lli-btn-icon").Click()
                try:
                    self.WaitFindElementByTagAndText("td", imoNo, 0, 2, 5)
                    return PageStatus.SuccessfulOperation
                except:
                    innerHtml = self.driver.find_element(By.TAG_NAME,"html").get_attribute("innerHTML")
                    if ("There is no data to display." in innerHtml):
                        return PageStatus.ShipNonExistent
                    else:
                        return PageStatus.SuccessfulOperation
    def Login(self):
        print("Login zzzz")

        wait = WebDriverWait(self.driver,30)
        loginButton = self.FindElementsById("Login")
        userButton = self.FindElementsByClassName("logged-as__prefix")
        if (len(loginButton)> 0):
            loginButton[0].Click()
            self.WaitFindElementByTag("input", 0, 2)
            inputForms = self.driver.find_element(By.TagName("input")
            inputForms[1].SendKeys(self.username)
            inputForms[2].SendKeys(self.password)
            buttonsLogin = self.driver.find_element(By.TagName("input")
            buttonsLogin.Where(x => x.GetAttribute("value") == "Login").ToList()[0].Click();
            return True

        elif (len(userButton)>0):
            return True

        elif (self.Url.Contains("signin")):
            self.WaitFindElementByTag("input", 0, 2)
            inputForms = self.driver.find_element(By.TAG_NAME,"input")

            inputForms[1].SendKeys(self.username)
            inputForms[2].SendKeys(self.username)

            buttonsLogin = self.driver.find_element(By.TAG_NAME,"input")
            buttonsLogin.Where(x => x.GetAttribute("value") == "Login").ToList()[0].Click()
            return True
        else:
            return False



    def GoToLloydsMainPage(self):

            print("GoToLloydsMainPage zzzz")
            Navigate().GoToUrl(self.lloydsWebSite)

    def  WaitFindElementByClassName(self,className,attempt,maxAttempt):
            print("WaitFindElementByClassName zzzz")
            while(len(self.FindElementsByClassName(className))>0):
                x=1
            #wait.Until(x => ((ChromeDriver)x).FindElementsByClassName(className).Count() > 0)

    def GoToLoginPage(self):
            print("GoToLoginPage")
            loginButton = self.FindElementsById("Login")
            if (len(loginButton) > 0):
                loginButton.First().Click()

    def WaitFindElementByTagAndText(self,tag,text,attempt,maxAttempt,timeOutTime):
            print("WaitFindElementByTagAndText zzzz")
            try:
                #wait.Timeout = new TimeSpan(0, 0, timeOutTime)
                time.sleep(timeOutTime)
                #wait.Until(x => ((ChromeDriver)x).FindElementsByTagName(tag).Where(y => y.Text == text).Count() > 0)
            except:
                if(attempt > maxAttempt):
                    #throw e
                    print('except:')
                WaitFindElementByTagAndText(self,tag, text, attempt + 1, maxAttempt, timeOutTime)


    def WaitFindElementByTagAndText1(self,tag,text,attempt,maxAttempt):

            print("WaitFindElementByTagAndText zzzz")
            try:
                wait.Until(x => ((ChromeDriver)x).FindElementsByTagName(tag).Where(y => text.Contains(y.Text)).Count() > 0)
            except:
                if (attempt > maxAttempt):
                    print('except:')
                WaitFindElementByTagAndText(tag, text, attempt + 1, maxAttempt)

    def ParseLloydsdatetimeAISSignalSent(self,aisSignalSentText):
        print("ParseLloydsdatetimeAISSignalSent zzzz")
        splitHourDate = aisSignalSentText.strip().replace('GMTGMT', "GMT").split('GMT')
        #splitHourDate = aisSignalSentText.Split{"GMT"}, StringSplitOptions.RemoveEmptyEntries)
        if (len(splitHourDate)>= 2):
            splitHourMinutes = splitHourDate[0].strip().Split(':')
            dateStringSplit = splitHourDate[1].Split('/')
            year = 0
            month = 0
            day = 0
            hour = 0
            minutes = 0
            if(int(isinstance(dateStringSplit[2].strip(),float))and(int(isinstance(dateStringSplit[1],float)))and int(isinstance(dateStringSplit[0],float))and\
               int(isinstance(splitHourMinutes[0].strip(),float)) and int(isinstance(splitHourMinutes[1].strip(), float))):

                year=int(isinstance(dateStringSplit[2].strip(),float))
                month = int(isinstance(dateStringSplit[1].strip(),float))
                day = int(isinstance(dateStringSplit[0].strip(),float))

                hour=int(isinstance(splitHourMinutes[0].strip(), float))
                minutes=int(isinstance(splitHourMinutes[1].strip(), float))

                return datetime(year+ 2000, month, day, hour, minutes, 0)

            else:
                return None
        else:
             return None

    # 需要Python3
    '''def foreach(self,function, iterator):
        for item in iterator:
            function(item)'''

    def CleanAISData(self,AISDataTable,instruction):
        print("CleanAISData zzzz")
        for i in range(len(AISDataTable)):
            row=AISDataTable[i]
            aNumber = 0
            aDate = datetime.now
            row["imo"] = instruction.imo
            (temp,aNumber)=self.ParseToFloat(row["Distance (nm)"])
            if(temp):
                row["Distance (nm)"] = aNumber
            else:
                #row["Distance (nm)"] = DBNull.Value
                row["Distance (nm)"] = None
            row["Date/Time"] = self.ParseLloydsdatetimeAISSignalSent(str(row["Date/Time"]))

            xy = self.ParseLongitudeAndLatitude(str(row["Lat/Lng Position"]))

            row["x"] = xy.Item1
            row["y"] = xy.Item2

            ETAnDestination = self.ParseLloydsETAandDestination(str(row["Destination"]))
            row["Destination"] = ETAnDestination.Item2
            row["ETA"] = ETAnDestination.Item1

            (temp, aNumber) = self.ParseToFloat(row["Heading"])
            if(temp):
                row["Heading"] = aNumber
            else:
                row["Heading"] = None

            (temp, aNumber) = self.ParseToFloat(row["Speed over ground"])
            if (temp):
                row["Speed over ground"] = aNumber
            else:
                row["Speed over ground"] = None

            (temp, aNumber) = self.ParseToFloat(row["Course over ground"])
            if (temp):
                row["Course over ground"] = aNumber
            else:
                row["Course over ground"] = None

            (temp, aNumber) = self.ParseToFloat(row["Draught (m)"])
            if (temp):
                row["Draught (m)"] = aNumber
            else:
                row["Draught (m)"] = None



    def ParseToFloat(self,numberAsString):
        print("ParseToFloat zzzz")
        numberAsString = numberAsString.replace( "[^0-9.,]","")
        #if (float.TryParse(numberAsString.strip(), out fl))
        if (isinstance(numberAsString.strip(),float)):
            f1=float(numberAsString.strip())
            return (True,f1)

        elif(isinstance(numberAsString.strip().replace(".", ","),float)):
            f1 = float(numberAsString.strip().replace(",", "."))
            return (True,f1)

        elif(isinstance(numberAsString.strip().replace(",", "."),float)):
            f1 = float(numberAsString.strip().replace(",", "."))
            return (True,f1)

        else:
            return False




    def ConvertToDecimalDegrees(self,degrees,isNegative):
        print("ConvertToDecimalDegrees zzzz")
        degreesOut = 0
        degreePart = 0
        minutesPart = 0
        secondsPart = 0

        #splittedString = degrees.Split({"°", " ", "'"}, StringSplitOptions.RemoveEmptyEntries)
        splittedString = degrees.split({"°", " ", "'"})

        if (self.ParseToFloat(splittedString[0])and self.ParseToFloat(splittedString[1])and self.ParseToFloat(splittedString[2])):
            degreePart=splittedString[0]
            minutesPart=splittedString[1]
            secondsPart=splittedString[2]
            degreesOut = degreePart + (minutesPart / float(60)) + (secondsPart / 3600)
            if isNegative:
                degreesOut = -degreesOut
            return degreesOut
        else:
            return None
            #return DBNone.Value

    def ParseLloydsETAandDestination(self,etaNDestinationString):
        print("ParseLloydsETAndDestination zzzz")
        #split1 = etaNDestinationString.Split({"ETA:"}, StringSplitOptions.RemoveEmptyEntries)
        split1 = etaNDestinationString.strip().replace('ETA:ETA:',"ETA:").split('ETA:')
        date = datetime.now
        if (split1.Count() >= 2):
            destination = split1[0].strip()
            dateStr = split1[1].strip().replace(" ", "-")
            dateSplit = dateStr.Split('-')
            if (len(dateSplit)>= 3):
                if dateSplit[1].ToLower()=="jan":
                    dateSplit[1] = "01"
                elif dateSplit[1].ToLower()=="feb":
                    dateSplit[1] = "02"
                elif dateSplit[1].ToLower()=="mar":
                    dateSplit[1] = "03"
                elif dateSplit[1].ToLower()=="apr":
                    dateSplit[1] = "04"
                elif dateSplit[1].ToLower()=="may":
                    dateSplit[1] = "05"
                elif dateSplit[1].ToLower()=="jun":
                    dateSplit[1] = "06"
                elif dateSplit[1].ToLower()=="jul":
                    dateSplit[1] = "07"
                elif dateSplit[1].ToLower()=="aug":
                    dateSplit[1] = "08"
                elif dateSplit[1].ToLower()=="sep":
                    dateSplit[1] = "09"
                elif dateSplit[1].ToLower()=="oct":
                    dateSplit[1] = "10"
                elif dateSplit[1].ToLower()=="nov":
                    dateSplit[1] = "11"
                elif dateSplit[1].ToLower()=="dec":
                    dateSplit[1] = "12"
                else:
                    dateSplit[1] = dateSplit[1]

            if (datetime.strptime(dateSplit,"%d-%m-%M")):
                 return (date,destination)
            else :
                return (None, destination)
    def CloseDriver(self):
         Close()

    #def datetime(self):