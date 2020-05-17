#import OpenQA
import argparse
from selenium import webdriver
#import selenium.webdriver.chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from enum import Enum
import time
from pandas import pandas
import numpy as np
import urllib.request
#from urllib.request import urlopen
from bs4 import BeautifulSoup
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

class LloydsBrowserDriver():
#class LloydsBrowserDriver():
    def __init__(self):
        self.__key = 'init'

    lloydsWebSite="https://www.lloydslistintelligence.com/"
    #wait
    Url=requests.get(lloydsWebSite)
    driver = webdriver.Chrome()

    def get_wait(self):
        return self.wait
    def set_wait(self, wait):
        self.wait = wait
    wait=property(get_wait,set_wait)

    username=""
    password=""

    def get_password(self):
        return self.password
    def set_password(self,password):
        self.password=password

    #password = property(get_password, set_password)

    def get_username(self):
        return self.username

    def set_username(self,username):
        self.username=username

    #username = property(get_username,set_username,)

    def get_PageStatus(self):
        return self.PageStatus

    def set_PageStatus(self,PageStatus):
        self.PageStatus =PageStatus

    def LloydsBrowserDriver(self,service,options,username,password):#两个没用上
        time.sleep(30)#???
        self.username = username
        self.password = password

    def SetUpLloydsBrowserDriver(self,username,password):
        print("SetUpLloydsBrowserDriver zzzz")

        # c_service = Service('xxx')
        # c_service.command_line_args()
        # c_service.start()
        # #driver = webdriver.Chrome()
        # self.driver.get("http://www.baidu.com")

        #chromeServices = ChromeDriverService.CreateDefaultService()
        #chromeServices = self.driver.service()

        #有问题
        #chromeServices = self.driver.service()
        chromeServices= Service.start
        chromeServices.HideCommandPromptWindow = True
        chromeServices.SuppressInitialDiagnosticInformation = True

        opt = webdriver.ChromeOptions() #浏览器选项??
        #parser = argparse.ArgumentParser()
        opt.add_argument("--user-data-dir=c:\\Historical Parser")
        opt.add_argument("--dns-prefetch-disable")
        opt.add_argument("start-maximized")
        opt.add_argument("disable-infobars")
        #parser.add_userProfilePreference("safebrowsing.enabled", True)
        opt.add_experimental_option("safebrowsing.enabled", True)
        #瞎写的
        return self.LloydsBrowserDriver(chromeServices, opt, username, password)


    def GetShipData(self,instruction):
        print("GetShipData zzzz")
        imoNo = str(instruction.imo)

        #self.PageStatus = LloydsBrowserDriver.GoToShipMovements(instruction)
        self.PageStatus = self.GoToShipMovements(instruction)
        table = pandas.DataFrame()

        if (self.PageStatus == PageStatus.SuccessfulOperation.value):
            table = self.FillDataTable(instruction)
            self.CleanAISData(table, instruction)
        return (table, self.PageStatus)

    def GoToShipMovements(self,instruction):

        print("GoToShipMovements zzz")
        result = PageStatus.SuccessfulOperation.value
        imoNo = str(instruction.imo)
        time.sleep(2)
        
        if (self.Url in {"https://www.lloydslistintelligence.com/","https://www.lloydslistintelligence.com"}):
            time.sleep(0.5)
            result = self.GoToShipPageFromMainPage(imoNo)
            print("GoToShipPageFromMainPage")
        elif (not("?term" in self.Url) and ("vessel" in self.Url) and ("overview" in self.Url or "movements" in self.Url)):
            time.sleep(0.5)
            result = self.GoToShipFromShipPage(imoNo)
            print("GoToShipFromShipPage")
        else:
            print("else")
            time.sleep(0.5)
            self.GoToLloydsMainPage()
            self.Login()
            result = self.GoToShipPageFromMainPage(imoNo)
        if (result == PageStatus.SuccessfulOperation.value):
            print("GoToShipMovements zzzz PageStatus.SuccessfulOperation.value")
            self.WaitFindElementByTagAndText("a", "Vessels", 0, 2, 2)
            if ("term" in self.Url):
                time.sleep(0.5)
                result = self.GoToShipFromTermPage(imoNo)
                print("GoToShipFromTermPage")
            time.sleep(0.5)
            print("GoToAISDataPageFromShipPage")
            if (self.CheckIfCorrectShipPage(imoNo)):
                result = self.GoToAISDataPageFromShipPage()
            else:
                return PageStatus.Error.value
        print("GoToShipMovements zzzz PageStatus.Error.value")
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


    #driver.page_source = driver.get('http://culture.dzwww.com/wx/')

    def FillDataTable(self,instruction):
        print("FileDataTable zzzz")
        tableData = pandas.DataFrame()
        #driver = webdriver.Chrome()
        self.SetHeaders(tableData)
        date = datetime.now
        self.ChangeFromToDate(instruction.startDate, instruction.endDate)
        self.AddAISDataToTable(tableData, instruction)
        isDataTransferred = False
        isDateChanged = False
        attempts = 2

        checkIfNoDataTextInTable = ("There is no data to display." in self.driver.page_source)
        if checkIfNoDataTextInTable:
                self.PageStatus = PageStatus.NoDataFound.value
        return tableData

    def ChangeFromToDate(self,fromDate, toDate):
        print("ChageFromToDate zzzz")
        dateElements = self.driver.find_elements(By.CLASS_NAME,"react-datepicker-wrapper")
        fromDateBox = dateElements[0].find_element(By.TAG_NAME("input"))
        toDateBox = dateElements[1].find_element(By.TAG_NAME("input"))
        fromDate=str(fromDate)
        toDate = str(toDate)


        fromDateBox.click()
        fromDateBox.clear()
        time.sleep(0.5)
        #fromDateBox.send_keys(str(np.repeat(Keys.Backspace.ToString(),22)))
        fromDateBox.send_keys(str(np.repeat(str(Keys.BACKSPACE),22)))
        fromDateBox.send_keys(time.strptime(fromDate,"%d/%m/%y").replace(".", "/") + "\n\r\n")
        time.sleep(0.5)
        dateElements[0].click()
        time.sleep(0.5)

        toDateBox.click()
        toDateBox.clear()
        time.sleep(0.5)

        #toDateBox.send_keys(string(Concat(Enumerable.Repeat(Keys.Backspace.ToString(), 22))))
        toDateBox.send_keys(str(np.repeat(str(Keys.BACKSPACE),22)))
        time.sleep(0.5)
        toDateBox.send_keys(time.strptime(fromDate,"%d/%m/%y").replace(".", "/") + "\n\r\n")
        time.sleep(0.5)
        dateElements[1].click()

        #wait.Timeout = TimeSpan(0, 0, 20)
        time.sleep(20)
        #wait.Until(x= > !driver.page_source.Contains("Loading data"))
        #wait.Timeout = new TimeSpan(0, 0, 30)
        time.sleep(30)
        #wait=timedelta(seconds=20)
        time.sleep(20)
        while("Loading data" in self.driver.page_source):
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
        self.clickNextPage()
        newPageNo = self.GetPageCurrentPage()
        return newPageNo > currentPageNo

    def  clickNextPage(self):
        print("clickNextPage zzzz")
        disclaimerBanners = self.driver.find_elements(By.CLASS_NAME("flaticon-cross"))
        if (len(disclaimerBanners)!= 0):
            disclaimerBanners[0].click()
        buttons = self.driver.find_element(By.CLASS_NAME("lli-grid-pager__link--next"))
        if (not("disabled" in buttons.get_attribute("class"))):
            buttons.click()

    def AddAISDataToTable(self,dataTable,instruction):
        print("AddAISDataToTable zzzz")
        time.sleep(2)
        #wait.Timeout = new TimeSpan(0, 0, 1)
        time.sleep(1)
        #driver.page_source.Contains("loading data")
        #wait.Timeout = new TimeSpan(0, 0, 30)
        time.sleep(30)
        tableString = self.driver.find_element(By.TAG_NAME,"table").get_attribute("innerHTML")
        #htmlDoc = HtmlAgilityPack.HtmlDocument()
        soup = BeautifulSoup()

        if (not("There is no data to display."in tableString)):
            #htmlDoc.LoadHtml(tableString)
            table=soup.find('table','tr').descendants


            #table = htmlDoc.DocumentNode.Descendants("tr").Select(x => x.Descendants("td").Select(y => y.InnerText).ToList()).ToList()
            ##删掉了select
            headers = list(self.driver.find_elements(By.TAG_NAME,"th"))

            #table = table.Where(x => x.Count > 0).ToList()
            table=list(table)
            #foreach (row in table):
            for i in range(len(table)):
                row=table[i]
                print("foreach row ------------")
                date = datetime.now
                if ("Date/Time" in headers and len(row) > 6):
                    print("foreach row -----in-------{0}",str(row[headers.index("Date/Time")]))

                    # if (float.TryParse(numberAsString.strip(), out fl))
                    #if (isinstance(numberAsString.strip(), float)):
                    #if (DateTime.TryParse(row[headers.IndexOf("Date/Time")].ToString(), out date)):
                    if (isinstance(str(row[headers.index("Date/Time")]),date)):#??
                        newRow = dataTable.NewRow()
                        print("foreach     colum --------row.count-{0:g}", row.Count)
                        for columnNo in range(len(row)):
                            #for (int columnNo = 0; columnNo < row.Count; columnNo++):
                                columnName = headers[columnNo]
                                print("foreach     colum ----------lll--{0:g}, {0:g}", columnNo, len(row))
                                if (len(row)> columnNo):
                                    print("foreach     colum ------------  nooooooooooo")
                                    newRow[columnName] = row[columnNo]
                        dataTable.Rows.Add(newRow)
                else:
                        print("AddAISDataToTable llll When adding data the row was found to be to short.")
                        #print("When adding data the row was found to be to short.")

    def GoToShipFromTermPage(self,imoNo):
        print("GoToShipFromTermPage zzzz")
        self.WaitFindElementByTagAndText("a", "Vessels", 0, 2, 2)
        #tableRows = FindElementsByTagName("tr")
        tableRows = self.driver.find_elements(By.TAG_NAME,"tr")
        tableRows=list(tableRows)
        #foreach(row in tableRows):
        for i in range(len(tableRows)):
            #columnsWithImo = tableRows[i].find_elements(By.TAG_NAME("td")).Where(x= > x.Text == imoNo).ToList()
            columnsWithImo = []
            row=tableRows[i].find_elements(By.TAG_NAME, "td")
            for j in  range(len(row)):
                if(row[j].text==imoNo):
                    a=tableRows[i].find_elements(By.TAG_NAME("td"))
                    columnsWithImo.append(tableRows[i].find_elements(By.TAG_NAME("td")))
            if(len(columnsWithImo)> 0):
                #row.find_elements(By.TAG_NAME,"a").Where(x = > x.GetAttribute("href").Contains("vessel")).first().click()
                a=tableRows[i].find_elements(By.TAG_NAME, "td")
                for j in range(len(a)):
                    if ("vessel" in a[j].get_attribute("href")):
                        a[j].click()
                        break
                return PageStatus.SuccessfulOperation.value
        return PageStatus.ShipNonExistent.value

    def GoToShipFromShipPage(self,imoNo):
        print("GoToShipFromShipPage zzzz")
        self.driver.find_element(By.CLASS_NAME,"lli-searchform__input").click()
        #self.driver.find_element(By.CLASS_NAME,"lli-searchform__input").send_keys(string.join("",\
        #    Enumerable.repeat(Keys.Backspace.ToString(), 1.5 + (random.random()))))
        self.driver.find_element(By.CLASS_NAME,"lli-searchform__input").send_keys(\
            np.repeat(str("\b"), 15 + 10*(random.random())))
        self.driver.find_element(By.CLASS_NAME,"lli-searchform__input").send_keys(imoNo)

        time.sleep(0.5 + random.uniform(0,2))
        self.driver.find_element(By.CLASS_NAME,"lli-searchform__button").click()
        return PageStatus.SuccessfulOperation.value


    def ParseLongitudeAndLatitude(self,longOrLat):
        print("SetUpLloydsBrowserDriver zzzz")
        # split1 = etaNDestinationString.Split({"ETA:"}, StringSplitOptions.RemoveEmptyEntries)
        #split1 = etaNDestinationString.strip().replace('ETA:ETA:', "ETA:").split('ETA:')

        #splittedString =longOrLat.Split({ "N", "S" }, StringSplitOptions.RemoveEmptyEntries)
        splittedString = longOrLat.strip().split({"N", "S"})#???
        if(len(splittedString)>2):
            latitudeString = splittedString[0]
            longitudeString = splittedString[1]

            isSouth = longOrLat.Contains("S")
            isWest = longOrLat.Contains("W")

            y = self.ConvertToDecimalDegrees(latitudeString, isSouth)
            x = self.ConvertToDecimalDegrees(longitudeString, isWest)
            return (x,y)
        else:
            return (None, None)

    def GoToAISDataPageFromShipPage(self):
        print("GoToAISDataPageFromShipPage zzzz")
        self.WaitFindElementByTagAndText("a", "Movements", 0, 5, 5)
        a1=self.driver.find_elements(By.TAG_NAME,"a")
        a2=[]
        la1=0
        for i in range(len(a1)):
            #FindElementsByTagName
            if(a1[i].text == "Movements"):
                a2[la1]=a1[i]
                la1=la1+1
        a2[0].click()
        print("GoToAISDataPageFromShipPage zzzz Movements clicked")
        self.WaitFindElementByTagAndText("h1", "Ports and Passings", 0, 5, 5)

        #self.driver.find_elements(By.TAG_NAME("button").Where(x => x.Text == "AIS Positions").First().click()
        AIS1=self.driver.find_elements(By.TAG_NAME,"button")
        AIS2=[]
        la1 = 0
        for i in range(len(AIS1)):
            if (AIS1[i].text == "AIS Positions"):
                AIS2[la1] = AIS1[i]
                la1 = la1 + 1
        AIS2[0].click()

        print("GoToAISDataPageFromShipPage zzzz AIS Positions clicked")
        self.WaitFindElementByTagAndText("h1", "AIS Positions", 0, 5, 5)
        print("GoToAISDataPageFromShipPage zzzz AIS Positions finished")
        return PageStatus.SuccessfulOperation.value

    def CheckIfCorrectShipPage(self,imoNo):
        print("CheckIfCorrentShipPage zzzz")
        while(len(self.driver.find_elements(By.CLASS_NAME,"lli-infobar"))> 0):
            x=1
        imoInInfo = self.driver.find_element(By.CLASS_NAME,"lli-infobar").find_elements(By.TAG_NAME,("div"))[2].text
        imoInInfo1=[]
        for i in range(len(imoInInfo)):
            if(imoInInfo.isdigit()):
                imoInInfo1.append(str(imoInInfo[i]))
        str1=""
        imo = str1.join(imoInInfo1)
        return imoNo == imo

    def GoToShipPageFromMainPage(self,imoNo):
            print("GoToShipPageFromMainPage zzzz")
            time.sleep(2)
            if ("signin" in self.Url):
                self.Login()
                return self.GoToShipPageFromMainPage(imoNo)
            else:
                #self.driver.navigate().GoToself.Url("https://www.lloydslistintelligence.com/vessels/")
                #self.driver.navigate().to("https://www.lloydslistintelligence.com/vessels/")
                self.driver.get("https://www.lloydslistintelligence.com/vessels/")
                time.sleep(0.5+random.uniform(0,1))
                if ("signin"in self.Url):
                    self.Login()

                time.sleep(random.random(1))#???
                self.driver.find_element(By.CLASS_NAME,"lli-searchform__input").send_keys(imoNo)
                self.driver.find_element(By.CLASS_NAME,"lli-btn-icon").click()
                try:
                    self.WaitFindElementByTagAndText("td", imoNo, 0, 2, 5)
                    return PageStatus.SuccessfulOperation.value
                except:
                    innerHtml = self.driver.find_element(By.TAG_NAME,"html").get_attribute("innerHTML")
                    if ("There is no data to display." in innerHtml):
                        return PageStatus.ShipNonExistent.value
                    else:
                        return PageStatus.SuccessfulOperation.value
    def Login(self):
        print("Login zzzz")

        wait = WebDriverWait(self.driver,30)
        loginButton = self.driver.find_elements(By.ID, "Login")
        #loginButton = self.FindElementsById("Login")
        userButton = self.driver.find_elements(By.CLASS_NAME,"logged-as__prefix")
        if (len(loginButton)> 0):
            loginButton[0].click()
            self.WaitFindElementByTag("input", 0, 2)
            inputForms = self.driver.find_elements(By.TAG_NAME,"input")

            inputForms[1].send_keys(self.username)
            inputForms[2].send_keys(self.password)

            buttonsLogin = self.driver.find_elements(By.TAG_NAME,"input")
            #buttonsLogin.Where(x => x.GetAttribute("value") == "Login").ToList()[0].click();
            buttonsLogin1 = []
            # buttonsLogin.Where(x => x.GetAttribute("value") == "Login").ToList()[0].click()
            for i in range(len(buttonsLogin)):
                if (buttonsLogin[i].get_attribute("value") == "Login"):
                    buttonsLogin1.append(buttonsLogin[i])
            buttonsLogin1 = list(buttonsLogin1)
            buttonsLogin1[0].click()
            return True

        elif (len(userButton)>0):
            return True

        elif ("signin" in self.Url):
            self.WaitFindElementByTag("input", 0, 2)
            inputForms = self.driver.find_elements(By.TAG_NAME,"input")

            inputForms[1].send_keys(self.username)
            inputForms[2].send_keys(self.username)

            buttonsLogin = self.driver.find_element(By.TAG_NAME,"input")

            #buttonsLogin1=[]
            #buttonsLogin.Where(x => x.GetAttribute("value") == "Login").ToList()[0].click()
            #for i in range(buttonsLogin.size):
            #for element in buttonsLogin:
            if(buttonsLogin.get_attribute("value")=="Login"):
                buttonsLogin.click()
            #buttonsLogin1 = list(buttonsLogin1)
            #buttonsLogin1[0].click()
            return True
        else:
            return False



    def GoToLloydsMainPage(self):

            print("GoToLloydsMainPage zzzz")
            #webdriver.navigate().GoToself.Url(self.lloydsWebSite)
            self.driver.get(self.lloydsWebSite)

    def  WaitFindElementByClassName(self,className,attempt,maxAttempt):
            print("WaitFindElementByClassName zzzz")
            while(len(self.driver.find_elements(By.CLASS_NAME,className))>0):
                x=1
            #wait.Until(x => ((ChromeDriver)x).find_elementsaaa(className).Count() > 0)


    def WaitFindElementByTag(self,tag,attempt,maxAttempt):
        print("WaitFindElementByTag zzzz")
        try:
            # wait.Timeout = new TimeSpan(0, 0, timeOutTime)
            # wait.Until(x => ((ChromeDriver)x).FindElementsByTagName(tag).Where(y => y.Text == text).Count() > 0)

            #x = self.driver.find_elements(By.TAG_NAME, tag).where(y.Text == text)
            x=[]
            x1 = self.driver.find_elements(By.TAG_NAME, tag)
            for i in range(len(x1)):
                if(x1[i].text):
                    x.append(x1[i])
            while (len(x) <= 0):
                #x = self.driver.find_elements(By.TAG_NAME, tag).where(y.Text == text)
                x1 = self.driver.find_elements(By.TAG_NAME, tag)
                for i in range(len(x1)):
                    if (x1[i].text):
                        x.append(x1[i])
        except:
            if (attempt > maxAttempt):
                # throw e
                print('except:')
            self.WaitFindElementByTag(tag, attempt + 1, maxAttempt)

    def GoToLoginPage(self):
            print("GoToLoginPage")
            loginButton = self.driver.find_elements(By.ID,"Login")
            if (len(loginButton) > 0):
                #loginButton.First().click()
                loginButton[0].click()

    def WaitFindElementByTagAndText(self,tag,text,attempt,maxAttempt,timeOutTime):
            print("WaitFindElementByTagAndText zzzz")
            try:
                #wait.Timeout = new TimeSpan(0, 0, timeOutTime)
                time.sleep(timeOutTime)
                #wait.Until(x => ((ChromeDriver)x).FindElementsByTagName(tag).Where(y => y.Text == text).Count() > 0)
                x=self.driver.find_elements(By.TAG_NAME,tag)
                y=[]
                for i in range(len(x)):
                    if(x[i].text==text):
                        y.append(x[i])
                while(len(y)<=0):
                    x=self.driver.find_elements(By.TAG_NAME,tag)
                    for i in range(len(x)):
                        if (x[i].text == text):
                            y.append(x[i])
            except:
                if(attempt > maxAttempt):
                    #throw e
                    print('except:')
                self.WaitFindElementByTagAndText(tag,text, attempt + 1, maxAttempt, timeOutTime)

    def WaitFindElementByTagAndText1(self,tag,text,attempt,maxAttempt):

            print("WaitFindElementByTagAndText1 zzzz")
            try:
                #wait.Until(x => ((ChromeDriver)x).FindElementsByTagName(tag).Where(y => text.Contains(y.Text)).Count() > 0)
                x = self.driver.find_elements(By.TAG_NAME, tag)
                y = []
                for i in range(len(x)):
                    if (x[i].text in text):
                        y.append(x[i])
                while (len(y) <= 0):
                    x = self.driver.find_elements(By.TAG_NAME, tag)
                    for i in range(len(x)):
                        if (x[i].text == text):
                            y.append(x[i])
            except:
                if (attempt > maxAttempt):
                    print('except:')
                self.WaitFindElementByTagAndText1(tag, text, attempt + 1, maxAttempt)

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

            xy = self.ParseLongitudeAndLatitude(row["Lat/Lng Position"])

            row["x"] = xy[0]
            row["y"] = xy[1]

            ETAnDestination = self.ParseLloydsETAandDestination(str(row["Destination"]))
            row["Destination"] = ETAnDestination[1]
            row["ETA"] = ETAnDestination[0]

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
         self.driver.close()

    #def datetime(self):