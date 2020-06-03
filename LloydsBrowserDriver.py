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
    ShipNonExistent=0
    NoDataFound=1
    SuccessfulOperation=2
    DataFound=3
    Error=4

class LloydsBrowserDriver():
#class LloydsBrowserDriver():
    def __init__(self):
        self.__key = 'init'
        self.username = 'liboyang@lll13.onexmail.com'
        self.password = 'li123456'
        self.wait = None
        self.PageStatus = None
    #存疑


    def get_key(self):
        return self.__key
    def set_key(self,key):
        self.__key=key

    lloydsWebSite="https://www.lloydslistintelligence.com/"
    #wait

    driver = webdriver.Chrome()
    time.sleep(1)
    driver.get(lloydsWebSite)
    time.sleep(1)
    Url = driver.current_url
    print("Url",Url)

    def get_wait(self):
        return self.wait
    def set_wait(self, wait):
        self.wait = wait
    #wait=property(get_wait , set_wait)


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
        #改回来
        #self.wait = time.sleep(30)#???
        self.username = username
        self.password = password

    def SetUpLloydsBrowserDriver(self,username,password):
        print("SetUpLloydsBrowserDriver zzzz")
        #chromeServices = ChromeDriverService.CreateDefaultService()
        #chromeServices = self.driver.service()

        #有问题
        #chromeServices = self.driver.service()
        chromeServices= Service.start
        chromeServices.HideCommandPromptWindow = True
        chromeServices.SuppressInitialDiagnosticInformation = True

        opt = webdriver.ChromeOptions() #浏览器选项??
        #parser = argparse.ArgumentParser()
        print("到这里了1！")
        opt.add_argument("--user-data-dir=c:\\Historical Parser")
        opt.add_argument("--dns-prefetch-disable")
        opt.add_argument("start-maximized")
        opt.add_argument("disable-infobars")
        #parser.add_userProfilePreference("safebrowsing.enabled", True)
        #opt.add_argument("safebrowsing.enabled", True)
        opt.add_experimental_option("safebrowsing.enabled", True)
        #瞎写的
        print("到这里了2！")
        return self.LloydsBrowserDriver(chromeServices, opt, username, password)


    def GetShipData(self,instruction):
        print("GetShipData zzzz")
        imoNo = str(instruction.imo)

        #self.PageStatus = LloydsBrowserDriver.GoToShipMovements(instruction)
        self.PageStatus = self.GoToShipMovements(instruction)
        table = pandas.DataFrame()

        if (self.PageStatus == PageStatus.SuccessfulOperation.value):
            #??没搞懂
            table = self.FillDataTable(instruction)
            self.CleanAISData(table, instruction)
        return (table, self.PageStatus)

    def GoToShipMovements(self,instruction):

        print("GoToShipMovements zzz")
        result = PageStatus.SuccessfulOperation.value
        print("PageStatus.SuccessfulOperation.value:",result)
        imoNo = str(instruction.imo)
        time.sleep(2)
        print("self.Url:",self.Url)
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
            print("GoToShipMovements zzzz PageStatus.SuccessfulOperation.value",PageStatus.SuccessfulOperation.value)
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
        toDateBox.send_keys(time.strptime(toDate,"%d/%m/%y").replace(".", "/") + "\n\r\n")
        time.sleep(0.5)
        dateElements[1].click()

        #wait.Timeout = TimeSpan(0, 0, 20)
        #time.sleep(20)
        self.wait.timeout= 20
        #wait.Until(x= > !driver.page_source.Contains("Loading data"))
        self.wait.until(not "Loading data" in self.driver.page_source )
        #wait.Timeout = new TimeSpan(0, 0, 30)
        #time.sleep(30)
        self.wait.timeout =30
        #wait=timedelta(seconds=20)
        #time.sleep(20)
        # while("Loading data" in self.driver.page_source):
        #     x=1
        #time.sleep(20)
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

    def clickNextPage(self):
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
        #time.sleep(1)
        self.wait.timeout = 1
        #driver.page_source.Contains("loading data")
        #wait.Timeout = new TimeSpan(0, 0, 30)
        #time.sleep(30)
        self.wait.timeout = 30
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
                    if (str(row[headers.index("Date/Time")])):#??
                        date=time.strptime(str(row[headers.index("Date/Time")]), "%Y-%m-%d %H:%M:%S")
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
        tableRows = self.driver.find_elements(By.TAG_NAME,"tr")
        tableRows = list(tableRows)
        for i in range(len(tableRows)):
            columnsWithImo = []
            row=tableRows[i].find_elements(By.TAG_NAME, "td")
            for j in range(len(row)):
                if row[j].text == imoNo:
                    a=tableRows[i].find_elements(By.TAG_NAME("td"))
                    columnsWithImo.append(a)
            if len(columnsWithImo)> 0:
                a=tableRows[i].find_elements(By.TAG_NAME, "a")
                for j in range(len(a)):
                    if ("vessel" in a[j].get_attribute("href")):
                        a[j].click()#第一个点击
                        break
                return PageStatus.SuccessfulOperation.value
        return PageStatus.ShipNonExistent.value


    def GoToShipFromShipPage(self,imoNo):
        print("GoToShipFromShipPage zzzz")
        self.driver.find_element(By.CLASS_NAME,"lli-searchform__input").click()
        s1=""
        #!!!
        self.driver.find_element(By.CLASS_NAME,"lli-searchform__input").send_keys(
            s1.join(np.repeat(str("\b"), 15 + 10*(random.random()))))
        self.driver.find_element(By.CLASS_NAME,"lli-searchform__input").send_keys(imoNo)

        time.sleep(0.5 + random.uniform(0,2))
        self.driver.find_element(By.CLASS_NAME,"lli-searchform__button").click()
        return PageStatus.SuccessfulOperation.value



    def GoToAISDataPageFromShipPage(self):
        print("GoToAISDataPageFromShipPage zzzz")
        self.WaitFindElementByTagAndText("a", "Movements", 0, 5, 5)
        a1=self.driver.find_elements(By.TAG_NAME,"a")
        #a2=0
        #la1=0
        for i in range(len(a1)):
            #FindElementsByTagName
            if(a1[i].text == "Movements"):
                a2=a1[i]
                #la1=la1+1
                a2.click()
                break
        print("GoToAISDataPageFromShipPage zzzz Movements clicked")
        self.WaitFindElementByTagAndText("h1", "Ports and Passings", 0, 5, 5)

        #self.driver.find_elements(By.TAG_NAME("button").Where(x => x.Text == "AIS Positions").First().click()
        AIS1=self.driver.find_elements(By.TAG_NAME,"button")
        #AIS2=[]
        #la1 = 0
        for i in range(len(AIS1)):
            if (AIS1[i].text == "AIS Positions"):
                AIS2 = AIS1[i]
                AIS2.click()
                break
        print("GoToAISDataPageFromShipPage zzzz AIS Positions clicked")
        self.WaitFindElementByTagAndText("h1", "AIS Positions", 0, 5, 5)
        print("GoToAISDataPageFromShipPage zzzz AIS Positions finished")
        return PageStatus.SuccessfulOperation.value

    def CheckIfCorrectShipPage(self,imoNo):
        print("CheckIfCorrentShipPage zzzz")
        self.wait.until(len(self.driver.find_elements(By.CLASS_NAME,"lli-infobar"))> 0)
        #while(len(self.driver.find_elements(By.CLASS_NAME,"lli-infobar"))> 0):
         #   x=1
        imoInInfo = self.driver.find_element(By.CLASS_NAME,"lli-infobar").find_elements(By.TAG_NAME,("div"))[2].text
        #imoInInfo1=[]
        imo = ""
        for i in range(len(imoInInfo)):
            if(imoInInfo[i].isdigit()):
                #imoInInfo1.append(str(imoInInfo[i]))
                imo = imo.join(imoInInfo[i])
        return imoNo == imo

    def GoToShipPageFromMainPage(self,imoNo):
            print("GoToShipPageFromMainPage zzzz")
            time.sleep(2)
            self.Url = self.driver.current_url
            print("self.Url:", self.Url)
            if ("signin" in self.Url):
                self.Login()
                return self.GoToShipPageFromMainPage(imoNo)
            else:
                #self.driver.navigate().GoToself.Url("https://www.lloydslistintelligence.com/vessels/")
                #self.driver.navigate().to("https://www.lloydslistintelligence.com/vessels/")
                self.driver.get("https://www.lloydslistintelligence.com/vessels/")
                time.sleep(0.5+random.uniform(0,1))
                self.Url = self.driver.current_url
                print("self.Url:",self.Url)
                if ('signin' in self.Url):
                    print('signin成功！')
                    self.Login()

                time.sleep(random.random())#???
                print('imoNo:'+imoNo)
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

    def GoToLoginPage(self):
            print("GoToLoginPage")
            loginButton = self.driver.find_elements(By.ID,"Login")
            if (len(loginButton) > 0):
                #loginButton.First().click()
                loginButton[0].click()


    def Login(self):
        print("Login zzzz")

        self.wait = WebDriverWait(self.driver,30)
        ##自己判断是wait还是self！！
        loginButton = self.driver.find_elements(By.ID, "Login")
        print(loginButton)
        #loginButton = self.FindElementsById("Login")
        userButton = self.driver.find_elements(By.CLASS_NAME,"logged-as__prefix")
        print(userButton)

        if (len(loginButton)> 0):
            try:
                print("len(loginButton)："+str(len(loginButton)))
                loginButton[0].click()

                self.WaitFindElementByTag("input", 0, 2)

                print("wait完毕")
                time.sleep(5)
                inputForms = self.driver.find_elements(By.TAG_NAME,"input")
                print("len(inputForms)",len(inputForms))
                print("self.username:" + self.username)
                print("self.password:" + self.password)

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
            except:
                print("except")
            return True

        elif (len(userButton)>0):
            return True

        elif ("signin" in self.Url):
            self.WaitFindElementByTag("input", 0, 2)
            inputForms = self.driver.find_elements(By.TAG_NAME,"input")
            print("inputForms",inputForms)

            print("self.username:" + self.username)
            print("self.password:" + self.password)
            inputForms[1].send_keys(self.username)
            inputForms[2].send_keys(self.password)

            buttonsLogin = self.driver.find_elements(By.TAG_NAME,"input")
            print("buttonsLogin",buttonsLogin)

            #buttonsLogin1=[]
            #buttonsLogin.Where(x => x.GetAttribute("value") == "Login").ToList()[0].click()
            #for i in range(buttonsLogin.size):
            #for element in buttonsLogin:
            for i in range(len(buttonsLogin)):
                if(buttonsLogin[i].get_attribute("value")=="Login"):
                    buttonsLogin[i].click()
                    break

            #buttonsLogin1 = list(buttonsLogin1)
            #buttonsLogin1[0].click()
            print("true")
            return True
        else:
            return False



    def GoToLloydsMainPage(self):

            print("GoToLloydsMainPage zzzz")
            #webdriver.navigate().GoToself.Url(self.lloydsWebSite)#打开指定网址
            print(self.lloydsWebSite)
            self.driver.get(self.lloydsWebSite)

    def  WaitFindElementByClassName(self,className,attempt,maxAttempt):
            print("WaitFindElementByClassName zzzz")
            try:
                self.wait.until(len(self.driver.find_elements(By.CLASS_NAME,className))>0)
            except:
                if (attempt > maxAttempt):
                    # throw e
                    print('except:')
                    self.WaitFindElementByClassName(className, attempt+1, maxAttempt)
            #wait.Until(x => ((ChromeDriver)x).find_elementsaaa(className).Count() > 0)


    def WaitFindElementByTag(self,tag,attempt,maxAttempt):
        print("WaitFindElementByTag zzzz")
        try:
            print("tag:"+str(tag))
            #self.wait.until(len(self.driver.find_elements(By.TAG_NAME, tag)) > 0)

            # for i in range(len(x1)):
            #     if(x1[i].text):
            #         x.append(x1[i])
            # while (len(x) <= 0):
            #     #x = self.driver.find_elements(By.TAG_NAME, tag).where(y.Text == text)
            #     x1 = self.driver.find_elements(By.TAG_NAME, tag)
            #     for i in range(len(x1)):
            #         if (x1[i].text):
            #             x.append(x1[i])
        except:
            if (attempt > maxAttempt):
                # throw e
                print('except:')
            self.WaitFindElementByTagAndText(tag,tag, attempt + 1, maxAttempt,2)

    def WaitFindElementByTagAndText(self,tag,text,attempt,maxAttempt,timeOutTime):
            print("WaitFindElementByTagAndText zzzz")
            try:
                #wait.Timeout = new TimeSpan(0, 0, timeOutTime)
                #time.sleep(timeOutTime)
                self.wait.timeout=timeOutTime
                #wait.Until(x => ((ChromeDriver)x).FindElementsByTagName(tag).Where(y => y.Text == text).Count() > 0)
                x=self.driver.find_elements(By.TAG_NAME,tag)
                print(x)
                y=[]
                for i in range(len(x)):
                    if(x[i].text==text):
                        y.append(x[i])
                while(len(y)==0):
                    x=self.driver.find_elements(By.TAG_NAME,tag)
                    for i in range(len(x)):
                        if (x[i].text == text):
                            y.append(x[i])
                #self.wait.until(len(self.driver.find_elements(By.TAG_NAME,tag))>0)
            except:
                if(attempt > maxAttempt):
                    #throw e
                    print('except:')
                    return  # 自己加的
                self.WaitFindElementByTagAndText(tag,text, attempt + 1, maxAttempt, timeOutTime)

    def WaitFindElementByTagAndText1(self,tag,text,attempt,maxAttempt):

            print("WaitFindElementByTagAndText1 zzzz")
            try:
                #wait.Until(x => ((ChromeDriver)x).FindElementsByTagName(tag).Where(y => text.Contains(y.Text)).Count() > 0)
                x = self.driver.find_elements(By.TAG_NAME, tag)
                print(x)
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
                    return#自己加的
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
            if(int(dateStringSplit[2].strip())and(int(dateStringSplit[1]))and int(dateStringSplit[0])and\
               int(splitHourMinutes[0].strip()) and int(splitHourMinutes[1].strip())):

                year=int(dateStringSplit[2].strip())
                month = int(dateStringSplit[1].strip())
                day = int(dateStringSplit[0].strip())

                hour=int(splitHourMinutes[0].strip())
                minutes=int(splitHourMinutes[1].strip())

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
        #numberAsString = numberAsString.replace( "[^0-9.,]","")
        numberAsString = numberAsString.replace("0", "")
        numberAsString = numberAsString.replace("1", "")
        numberAsString = numberAsString.replace("2", "")
        numberAsString = numberAsString.replace("3", "")
        numberAsString = numberAsString.replace("4", "")
        numberAsString = numberAsString.replace("5", "")
        numberAsString = numberAsString.replace("6", "")
        numberAsString = numberAsString.replace("7", "")
        numberAsString = numberAsString.replace("8", "")
        numberAsString = numberAsString.replace("9", "")

        #if (float.TryParse(numberAsString.strip(), out fl))
        f1=0
        if (float(numberAsString.strip())):
            f1=float(numberAsString.strip())
            return (True,f1)

        elif(float(numberAsString.strip().replace(".", ","))):
            f1 = float(numberAsString.strip().replace(",", "."))
            return (True,f1)

        elif(float(numberAsString.strip().replace(",", "."))):#float.写法存疑
            f1 = float(numberAsString.strip().replace(",", "."))
            return (True,f1)

        else:
            return (False,f1)

    def ParseLongitudeAndLatitude(self,longOrLat):
        print("SetUpLloydsBrowserDriver zzzz")
        # split1 = etaNDestinationString.Split({"ETA:"}, StringSplitOptions.RemoveEmptyEntries)
        #split1 = etaNDestinationString.strip().replace('ETA:ETA:', "ETA:").split('ETA:')

        #splittedString =longOrLat.Split({ "N", "S" }, StringSplitOptions.RemoveEmptyEntries)
        splittedString = longOrLat.split({"N", "S"})#???
        while '' in splittedString:
            splittedString.remove('')

        if(len(splittedString)>2):
            latitudeString = splittedString[0]
            longitudeString = splittedString[1]

            isSouth = 'S' in longOrLat
            isWest = 'W' in longOrLat

            y = self.ConvertToDecimalDegrees(latitudeString, isSouth)
            x = self.ConvertToDecimalDegrees(longitudeString, isWest)
            return x , y
        else:
            return None, None


    def ConvertToDecimalDegrees(self,degrees,isNegative):
        print("ConvertToDecimalDegrees zzzz")
        degreesOut = 0
        degreePart = 0
        minutesPart = 0
        secondsPart = 0

        #splittedString = degrees.Split({"°", " ", "'"}, StringSplitOptions.RemoveEmptyEntries)
        splittedString = degrees.split({"°", " ", "'"})
        while '' in  splittedString:
            splittedString.remove('')
        x0, y0=  self.ParseToFloat(splittedString[0])
        x1, y1 = self.ParseToFloat(splittedString[1])
        x2, y2 = self.ParseToFloat(splittedString[2])

        if (x0 and x1 and x2):
            degreePart=y0
            minutesPart=y1
            secondsPart=y2

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
            destination = split1[0].strip()#去掉首尾空格
            dateStr = split1[1].strip().replace(" ", "-")
            dateSplit = dateStr.Split('-')
            if (len(dateSplit)>= 3):
                if dateSplit[1].lower() == "jan":
                    dateSplit[1] = "01"
                elif dateSplit[1].lower()=="feb":
                    dateSplit[1] = "02"
                elif dateSplit[1].lower()=="mar":
                    dateSplit[1] = "03"
                elif dateSplit[1].lower()=="apr":
                    dateSplit[1] = "04"
                elif dateSplit[1].lower()=="may":
                    dateSplit[1] = "05"
                elif dateSplit[1].lower()=="jun":
                    dateSplit[1] = "06"
                elif dateSplit[1].lower()=="jul":
                    dateSplit[1] = "07"
                elif dateSplit[1].lower()=="aug":
                    dateSplit[1] = "08"
                elif dateSplit[1].lower()=="sep":
                    dateSplit[1] = "09"
                elif dateSplit[1].lower()=="oct":
                    dateSplit[1] = "10"
                elif dateSplit[1].lower()=="nov":
                    dateSplit[1] = "11"
                elif dateSplit[1].lower()=="dec":
                    dateSplit[1] = "12"
                else:
                    dateSplit[1] = dateSplit[1]

            if (datetime.strptime(dateSplit,"%d-%m-%Y")):#null的含义
                date=datetime.strptime(dateSplit,"%d-%m-%Y")
                return date, destination
            else :
                return None, destination
    def CloseDriver(self):
         self.driver.close()

    #def datetime(self):