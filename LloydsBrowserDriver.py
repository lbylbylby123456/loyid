#import OpenQA
import argparse
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from enum import Enum
import time
from ChromeOptions import ChromeOptions
from DataTable import DataTable
from datetime import datetime
class PageStatus(Enum):
    ShipNonExistent=1
    NoDataFound=2
    SuccessfulOperation=3
    DataFound=4
    Error=5

class LloydsBrowserDriver(ChromeDriver):
    lloydsWebSite="https://www.lloydslistintelligence.com/"
    #wait
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
        driver = webdriver.Chrome()
        driver.get("http://www.baidu.com")

        chromeServices = ChromeDriverService.CreateDefaultService()
        chromeServices.HideCommandPromptWindow = True
        chromeServices.SuppressInitialDiagnosticInformation = True

        opt = ChromeOptions.now #浏览器选项??
        parser = argparse.ArgumentParser()
        parser.add_argument($"user-data-dir=c:\\Historical Parser")
        parser.add_argument("--dns-prefetch-disable")
        parser.add_argument("start-maximized")
        parser.add_argument("disable-infobars")
        parser.add_userProfilePreference("safebrowsing.enabled", True)
        return LloydsBrowserDriver(chromeServices, opt, username, password)


    def GetShipData(self,instruction):
        print("GetShipData zzzz")
        imoNo = instruction.imo.ToString()

        self.PageStatus = LloydsBrowserDriver.GoToShipMovements(instruction)
        table = DataTable.now

        if (self.PageStatus == PageStatus.SuccessfulOperation):
            table = FillDataTable(instruction)
            CleanAISData(table, instruction)
        return (table, self.PageStatus)

    def GoToShipMovements(self,instruction):

        print("GoToShipMovements zzz")
        result = PageStatus.SuccessfulOperation
        imoNo = instruction.imo.ToString()
        time.sleep(2)
        if (({"https://www.lloydslistintelligence.com/","https://www.lloydslistintelligence.com"}).Contains(Url)):
            time.sleep(0.5)
            result = GoToShipPageFromMainPage(imoNo)
            print("GoToShipPageFromMainPage")
        elif (!Url.Contains("?term") & & Url.Contains("vessel") & &(Url.Contains("overview") | | Url.Contains("movements"))):
            time.sleep(500)
            result = GoToShipFromShipPage(imoNo)
            print("GoToShipFromShipPage")
        else:
            print("else")
            time.sleep(0.5)
            GoToLloydsMainPage()
            Login()
            result = GoToShipPageFromMainPage(imoNo)
        if (result == PageStatus.SuccessfulOperation):
            print("GoToShipMovements zzzz PageStatus.SuccessfulOperation")
            WaitFindElementByTagAndText("a", "Vessels", 0, 2, 2)
            if (Url.Contains("term")):
                time.sleep(0.5)
                result = GoToShipFromTermPage(imoNo)
                print("GoToShipFromTermPage")
            time.sleep(0.5)
            print("GoToAISDataPageFromShipPage")
            if (CheckIfCorrectShipPage(imoNo)):
                result = GoToAISDataPageFromShipPage()
            else:
                return PageStatus.Error
        print("GoToShipMovements zzzz PageStatus.error");
        return result

    # 需要Python3

    def foreach(function, iterator):
        for item in iterator:
            function(item)

    def SetHeaders(self,table):
        print("SetHeaders zzz")
        table.Columns.Add("imo", typeof(int))
        table.Columns.Add("Current Position", typeof(string))
        table.Columns.Add("x", typeof(object))
        table.Columns.Add("y", typeof(object))
        table.Columns.Add("ETA", typeof(object))
        headers = FindElementsByTagName("th").Select(x= > x.Text).ToList()

        foreach(header,headers):
            table.Columns.Add(header)

    def FillDataTable(self,instruction):
        print("FileDataTable zzzz")
        tableData = new DataTable()
        SetHeaders(tableData)
        date = datetime.UtcNow
        ChangeFromToDate(instruction.startDate, instruction.endDate)
        AddAISDataToTable(tableData, instruction)
        isDataTransferred = False
        isDateChanged = False
        attempts = 2
        checkIfNoDataTextInTable = PageSource.Contains("There is no data to display.")
        if checkIfNoDataTextInTable:
                self.PageStatus = PageStatus.NoDataFound
        return tableData

    def ChangeFromToDate(self,fromDate, toDate):
        print("ChageFromToDate zzzz")
        dateElements = FindElementsByClassName("react-datepicker-wrapper")
        fromDateBox = dateElements[0].FindElement(By.TagName("input"))
        toDateBox = dateElements[1].FindElement(By.TagName("input"))

        fromDateBox.Click()
        fromDateBox.Clear()
        time.sleep(500)
        fromDateBox.SendKeys(string.concat(Enumerable.Repeat(Keys.Backspace.ToString(), 22)))
        fromDateBox.SendKeys(fromDate.ToString("dd/MM/yyyy").Replace(".", "/") + "\n\r\n")
        time.sleep(500)
        dateElements[0].Click()
        time.sleep(500)

        toDateBox.Click()
        toDateBox.Clear()
        time.sleep(500)

        toDateBox.SendKeys(string(Concat(Enumerable.Repeat(Keys.Backspace.ToString(), 22))))
        time.sleep(500)
        toDateBox.SendKeys(toDate.ToString("dd/MM/yyyy").Replace(".", "/") + "\n\r\n")
        time.sleep(500)
        dateElements[1].Click()

        wait.Timeout = new TimeSpan(0, 0, 20)
        wait.Until(x= > !PageSource.Contains("Loading data"))
        wait.Timeout = new TimeSpan(0, 0, 30)

    def GetPageCurrentPage():

        print("GetPageCurrentPage zzzz");
        pageNo = (int)Parse(FindElementByClassName("lli-grid-pager__input").GetAttribute("value"))
        return pageNo

    def GoToNextPage():
        print("GoToNextPage zzzz")
        currentPageNo = GetPageCurrentPage()
        ClickNextPage()
        newPageNo = GetPageCurrentPage()
        return newPageNo > currentPageNo

    def  ClickNextPage():
        print("ClickNextPage zzzz")
        disclaimerBanners = FindElementsByClassName("flaticon-cross")
        if (disclaimerBanners.Count != 0):
            disclaimerBanners.First().Click()
        buttons = FindElementByClassName("lli-grid-pager__link--next")
        if (!buttons.GetAttribute("class").Contains("disabled")):
            buttons.Click()
    def AddAISDataToTable(dataTable,instruction):
        print("AddAISDataToTable zzzz")
        time.sleep(2000)
        wait.Timeout = new TimeSpan(0, 0, 1)
        PageSource.Contains("loading data")
        wait.Timeout = new TimeSpan(0, 0, 30)
        tableString = FindElementByTagName("table").GetAttribute("innerHTML")
        HtmlAgilityPack.HtmlDocument
        htmlDoc = new
        HtmlAgilityPack.HtmlDocument()

        if (!tableString.Contains("There is no data to display.")):
            htmlDoc.LoadHtml(tableString)
            table = htmlDoc.DocumentNode.Descendants("tr").Select(x => x.Descendants("td").Select(y => y.InnerText).ToList()).ToList()
            headers = FindElementsByTagName("th").Select(x => x.Text).ToList()
            table = table.Where(x => x.Count > 0).ToList()

            foreach (row in table):
                    print("foreach row ------------")
                    date = datetime.now


    def GoToShipFromTermPage(self,imoNo):
        print("GoToShipFromTermPage zzzz")
        WaitFindElementByTagAndText("a", "Vessels", 0, 2, 2)
        tableRows = FindElementsByTagName("tr")
        foreach(row in tableRows):
            List < IWebElement > columnsWithImo = row.FindElements(By.TagName("td")).Where(x= > x.Text == imoNo).ToList()
        if (len(columnsWithImo) > 0):
           row.FindElements(By.TagName("a")).Where(x = > x.GetAttribute("href").Contains("vessel")).First().Click();
           return PageStatus.SuccessfulOperation
        return PageStatus.ShipNonExistent

    def GoToShipFromShipPage(self,imoNo):
        print("GoToShipFromShipPage zzzz")
        FindElement(By.ClassName("lli-searchform__input")).Click();
        FindElement(
            By.ClassName("lli-searchform__input")).SendKeys(string.Join("",
            Enumerable.Repeat(Keys.Backspace.ToString(), 15 + (new Random()).Next(10)))
            );
        FindElement(By.ClassName("lli-searchform__input")).SendKeys(imoNo);
        time.sleep(500 + (new Random()).Next(2000));
        FindElement(By.ClassName("lli-searchform__button")).Click();
        return PageStatus.SuccessfulOperation


    def ParseLongitudeAndLatitude(self,longOrLat):
        print("SetUpLloydsBrowserDriver zzzz")
        splittedString =longOrLat.Split(new string[] { "N", "S" }, StringSplitOptions.RemoveEmptyEntries)
        if(len(splittedString)>2):
            latitudeString = splittedString[0]
            longitudeString = splittedString[1]

            isSouth = longOrLat.Contains("S")
            isWest = longOrLat.Contains("W")

            y = ConvertToDecimalDegrees(latitudeString, isSouth)
            x = ConvertToDecimalDegrees(longitudeString, isWest)

            return (x,y)
        else:
            return (DBNull.Value, DBNull.Value)

    def GoToAISDataPageFromShipPage(self):
        print("GoToAISDataPageFromShipPage zzzz")
        WaitFindElementByTagAndText("a", "Movements", 0, 5, 5)
        FindElements(By.TagName("a")).Where(x => x.Text == "Movements").First().Click()
        print("GoToAISDataPageFromShipPage zzzz Movements clicked")
        WaitFindElementByTagAndText("h1", "Ports and Passings", 0, 5, 5)

        FindElementsByTagName("button").Where(x => x.Text == "AIS Positions").First().Click()
        print("GoToAISDataPageFromShipPage zzzz AIS Positions clicked")
        WaitFindElementByTagAndText("h1", "AIS Positions", 0, 5, 5)
        print("GoToAISDataPageFromShipPage zzzz AIS Positions finished")
        return PageStatus.SuccessfulOperation

    def CheckIfCorrectShipPage(self,imoNo):
        print("CheckIfCorrentShipPage zzzz");
        wait.Until(x= > ((ChromeDriver)x).FindElementsByClassName("lli-infobar").Count > 0)
        imoInInfo = FindElementByClassName("lli-infobar").FindElements(By.TagName("div"))[2].Text
        imo = string.Join("", imoInInfo.Where(x= > char.IsNumber(x)))
        return imoNo == imo

    def GoToShipPageFromMainPage(self,imoNo)
        {
            print("GoToShipPageFromMainPage zzzz")
            time.sleep(2)
            if (Url.Contains("signin")):
                Login();
                return GoToShipPageFromMainPage(imoNo)
            else:
                Navigate().GoToUrl("https://www.lloydslistintelligence.com/vessels/")
                time.sleep(500 + (new Random()).Next(1000))
                if (Url.Contains("signin")):
                    Login()
                time.sleep(random().Next(1000))#???
                FindElement(By.ClassName("lli-searchform__input")).SendKeys(imoNo)
                FindElement(By.ClassName("lli-btn-icon")).Click()
                try
                    WaitFindElementByTagAndText("td", imoNo, 0, 2, 5)
                    return PageStatus.SuccessfulOperation
                    innerHtml = FindElement(By.TagName("html")).GetAttribute("innerHTML")
                    if (innerHtml.Contains("There is no data to display."))
                        return PageStatus.ShipNonExistent
                    else:
                        return PageStatus.SuccessfulOperation
    def Login(self):
        print("Login zzzz")
        wait = new OpenQA.Selenium.Support.UI.WebDriverWait(this, TimeSpan.FromSeconds(30));
        loginButton = self.FindElementsById("Login");
        userButton = self.FindElementsByClassName("logged-as__prefix");
        if (len(loginButton)> 0):
            try
            {
                loginButton[0].Click();
                WaitFindElementByTag("input", 0, 2);
                ReadOnlyCollection<IWebElement> inputForms = this.FindElementsByTagName("input");

                inputForms[1].SendKeys(UserName);
                inputForms[2].SendKeys(PassWord);

                ReadOnlyCollection<IWebElement> buttonsLogin = this.FindElementsByTagName("input");
                buttonsLogin.Where(x => x.GetAttribute("value") == "Login").ToList()[0].Click();
            }
            catch (Exception e)
            {
            }

            return True;

        else if (userButton.Count > 0)

            //If already logged in return True.
            return True;

        else if (this.Url.Contains("signin")):
            WaitFindElementByTag("input", 0, 2);
            ReadOnlyCollection<IWebElement> inputForms = this.FindElementsByTagName("input");

            inputForms[1].SendKeys(UserName);
            inputForms[2].SendKeys(PassWord);

            ReadOnlyCollection<IWebElement> buttonsLogin = this.FindElementsByTagName("input");
            buttonsLogin.Where(x => x.GetAttribute("value") == "Login").ToList()[0].Click()
            return True
        else:
            return False;



    def GoToLoginPage(self):
            print("GoToLoginPage");
            loginButton = FindElementsById("Login");

            if (loginButton.Count > 0)
                loginButton.First().Click();
    def GoToLloydsMainPage(self):

            print("GoToLloydsMainPage zzzz");
            Navigate().GoToUrl(lloydsWebSite);

    def  WaitFindElementByClassName(self,className,attempt,maxAttempt):
            print("WaitFindElementByClassName zzzz");
            try
                wait.Until(x => ((ChromeDriver)x).FindElementsByClassName(className).Count() > 0);
            catch (Exception e)
                if (attempt > maxAttempt)
                    throw e
                WaitFindElementByClassName(className, attempt + 1, maxAttempt);

    def GoToLoginPage(self):

            print("GoToLoginPage");
            ReadOnlyCollection<IWebElement> loginButton = FindElementsById("Login")
            if (len(loginButton) > 0):
                loginButton.First().Click()

    def WaitFindElementByTagAndText(self,tag,text,attempt,maxAttempt,timeOutTime):
            print("WaitFindElementByTagAndText zzzz")
            try:
                wait.Timeout = new TimeSpan(0, 0, timeOutTime)
                wait.Until(x => ((ChromeDriver)x).FindElementsByTagName(tag).Where(y => y.Text == text).Count() > 0)
            except:
                if(attempt > maxAttempt):
                    #throw e
                WaitFindElementByTagAndText(tag, text, attempt + 1, maxAttempt, timeOutTime)


    def WaitFindElementByTagAndText(self,tag,text,attempt,maxAttempt):

            print("WaitFindElementByTagAndText zzzz")
            try:
                wait.Until(x => ((ChromeDriver)x).FindElementsByTagName(tag).Where(y => text.Contains(y.Text)).Count() > 0);
            catch (Exception e)
                if (attempt > maxAttempt):
                WaitFindElementByTagAndText(tag, text, attempt + 1, maxAttempt)

    def ParseLloydsdatetimeAISSignalSent(aisSignalSentText)
        print("ParseLloydsdatetimeAISSignalSent zzzz")
        splitHourDate = aisSignalSentText.Split{"GMT"}, StringSplitOptions.RemoveEmptyEntries)
        if (len(splitHourDate)>= 2):
            splitHourMinutes = splitHourDate[0].Trim().Split(':');
            dateStringSplit = splitHourDate[1].Split('/');
            year = 0;
            month = 0;
            day = 0;
            hour = 0;
            minutes = 0
            if(int(isinstance(dateStringSplit[2].Trim(),float))and(int(isinstance(dateStringSplit[1],float)))and int(isinstance(dateStringSplit[0],float))and \
            int(isinstance(splitHourMinutes[0].Trim(),float)) and int(isinstance(splitHourMinutes[1].Trim(), float))):

                year=int(isinstance(dateStringSplit[2].Trim(),float))
                month = int(isinstance(dateStringSplit[1].Trim(),float))
                day = int(isinstance(dateStringSplit[0].Trim(),float))

                hour=int(isinstance(splitHourMinutes[0].Trim(), float))
                minutes=int(isinstance(splitHourMinutes[1].Trim(), float))

                return datetime(year+ 2000, month, day, hour, minutes, 0)
            else:
                return DBNULL.Value
        else:
             return DBNULL.Value

    # 需要Python3
    '''def foreach(self,function, iterator):
        for item in iterator:
            function(item)'''

    def CleanAISData(self,AISDataTable,instruction):
        print("CleanAISData zzzz")
        while foreach(row):
            aNumber = 0
            aDate = new datetime()
            row["imo"] = instruction.imo
            if (ParseToFloat(row["Distance (nm)"].ToString(), out aNumber))
             row["Distance (nm)"] = aNumber
            else
             row["Distance (nm)"] = DBNull.Value

            row["Date/Time"] = ParseLloydsdatetimeAISSignalSent(row["Date/Time"].ToString())


            xy = ParseLongitudeAndLatitude(row["Lat/Lng Position"].ToString())
            row["x"] = xy.Item1;
            row["y"] = xy.Item2;

            ETAnDestination = ParseLloydsETAandDestination(row["Destination"].ToString());
            row["Destination"] = ETAnDestination.Item2
            row["ETA"] = ETAnDestination.Item1

            if (ParseToFloat(row["Heading"].ToString(), out aNumber)):
                row["Heading"] = aNumber
            else :
                row["Heading"] = DBNull.Value

            if (ParseToFloat(row["Speed over ground"].ToString(), out aNumber)):
                row["Speed over ground"] = aNumber
            else:
                row["Speed over ground"] = DBNull.Value

            if (ParseToFloat(row["Course over ground"].ToString(), out aNumber)):
                row["Course over ground"] = aNumber
            else:
                row["Course over ground"] = DBNull.Value

            if (ParseToFloat(row["Draught (m)"].ToString(), out aNumber)):
                row["Draught (m)"] = aNumber
            else:
                row["Draught (m)"] = DBNull.Value



    def ParseToFloat(self,numberAsString):
        print("ParseToFloat zzzz")
        numberAsString = System.Text.RegularExpressions.Regex.Replace(numberAsString, "[^0-9.,]", "")
        #if (float.TryParse(numberAsString.Trim(), out fl))
        if (isinstance(numberAsString.Trim(),float)):
            return True
        elif(isinstance(numberAsString.Trim().Replace(".", ","),float)):
            return True
        elif(isinstance(numberAsString.Trim().Replace(",", "."),float)):
            return True
        else:
            return False




    def ConvertToDecimalDegrees(self,degrees,isNegative):
        print("ConvertToDecimalDegrees zzzz");
        degreesOut = 0
        degreePart = 0
        minutesPart = 0
        secondsPart = 0

        splittedString = degrees.Split(new {"°", " ", "'"}, StringSplitOptions.RemoveEmptyEntries)

        if (ParseToFloat(splittedString[0], out degreePart)andParseToFloat(splittedString[1], out minutesPart)andParseToFloat(splittedString[2], out secondsPart)):
            degreesOut = degreePart + (minutesPart / 60f) + (secondsPart / 3600)
            if isNegative:
                degreesOut = -degreesOut
            return degreesOut
        else:
            return DBNull.Value

    def ParseLloydsETAandDestination(self,etaNDestinationString):
        print("ParseLloydsETAndDestination zzzz")
        split1 = etaNDestinationString.Split(new{"ETA:"}, StringSplitOptions.RemoveEmptyEntries)
        date = new datetime()
        if (split1.Count() >= 2):
            destination = split1[0].Trim()
            dateStr = split1[1].Trim().Replace(" ", "-")
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

            if (datetime.TryParseExact(string.Join("-", dateSplit), "dd-MM-yyyy", null, System.Globalization.datetimeStyles.None, out date)):
                 return (date,destination)
            else :
                return (DBNull.Value, destination)
    def CloseDriver(self):
         Close()

    #def datetime(self):