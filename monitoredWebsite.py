import re
import requests
import HTTPSwitcher
import threading
from datetime import datetime 
from datetime import timedelta
import time 
import threading
from databaseManagement import insertData, retrieveData, createDatabase, createTable


class monitoredWebsite : 

    def __init__(self, url = "", frequency = 10) : 

        """
        Attributes : 

        - url : url of the website (string)
        - frequency : interval in seconds at which the website will be checked (int)
        - status : current status for connection (bool)
        - statusCode : current HTTP connection code 
        """

        if self.urlFormat(url) : 
            self.url = url 
        else : 
            print('Please enter a valid URL')
            self.url = ""

        self.frequency = frequency 
        self.status = True 
        self.statusCode = 200  



    def urlFormat(self, url) : 

        """
        Inspects if the url attribute verifies the HTTP norms (code from https://stackoverflow.com/ )
        """

        regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' 
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' 
        r'(?::\d+)?' 
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return re.match(regex, url) is not None



    def isAvailable(self) : 

        """
        - Prints the connection status and the corresponding response code 
        - Returns True if the connection is successful, False otherwise 
        - Returns the connection status 
        - Returns the corresponding code for the connection status 

        HTTP response status : 

        1. Informational responses (100-199)
        2. Successful repsonses (200-299)
        3. Redirects (300-399)
        4. Client errors (400-499)
        5. Server errors (500-599)
        """

        if self.urlFormat(self.url) : 
            switcher = HTTPSwitcher.HTTPSwitcher(requests.get(self.url))

            if switcher.status()[1] >= 200 and switcher.status()[1] <= 299 : 
                self.status = True 
                self.statusCode = switcher.status()[1]

            else : 
                self.status = False 
                self.statusCode = switcher.status()[1]



    def responseTime(self) : 

        """
        Computes the response time of the website in seconds
        """

        if self.status : 
            response = requests.post(self.url)
            return response.elapsed.total_seconds()



    def getCurrentInfo(self) : 

        """
        Returns a tuple with real-time information about the website availability (bool), response code (int), response time (float), current time (datetime object)
        """

        self.isAvailable()
        return self.status, self.statusCode, self.responseTime(), datetime.now()



    def sendInfo(self, database) :

        """
        Sends current information to the database according to the 'frequency' attribute of the class 
        """ 

        while True : 
            availability = self.getCurrentInfo()[0]
            status_code = self.getCurrentInfo()[1]
            response_time = self.getCurrentInfo()[2]
        
            insertData(database, self.url, availability, status_code, response_time)

            time.sleep(self.frequency)



    def computeMetrics(self, database, computeInterval) : 

        """
        Computes the statistics (availability, average/max response time, response code) of a website within a given interval of time (considered to be in seconds)
        """


        timeIntervalDate = datetime.now() - timedelta(seconds=computeInterval)
        
        intervalData = retrieveData(database, self.url, timeIntervalDate)

        if intervalData is None : 
            return False
        if len(intervalData) == 0 : 
            return False 

        def mostFrequent(l) : 
            count = 0 
            num = l[0]
            for i in range(len(l)) : 
                freq = l.count(l[i])
                if freq > count : 
                    count = freq 
                    num = l[i] 
            return num  


        def stats(data) : 
            availabilitiesList = [d[0] for d in data if d[0] is not None]
            statuesCodesList = [d[1] for d in data if d[1] is not None]
            responseTimesList = [d[2] for d in data if d[2] is not None]

            averageAvailability = sum(availabilitiesList)/len(availabilitiesList)
            mostFrequentCode = mostFrequent(statuesCodesList)
            averageResponseTime = sum(responseTimesList)/len(responseTimesList)

            return  averageAvailability, mostFrequentCode, averageResponseTime


        alertMessage = ''
        finalMessage = ''


        if computeInterval == 120 : 
            if stats(intervalData)[0] <= 0.8 : 
                alertMessage = f'Website {self.url} is down.' + f'Availability = {stats(intervalData)[0]*100},% ' + f'time = {datetime.now()}  '

            if stats(intervalData)[0] > 0.8 and self.isAvailable()[0] == False : 
                alertMessage = f'Website {self.url} is recovering ' + f'since {datetime.now()}' 


        finalMessage = f'Statistics for website {self.url}' f' in the last {computeInterval} seconds : \n ' + f'Average availability : {stats(intervalData)[0]} \n ' + f'Most frequent HTTP response code : {stats(intervalData)[1]} \n ' + f'Average response time : {stats(intervalData)[2]} \n '

        print(finalMessage + alertMessage)
        return _, True 



    def getInfoWebsiteFrequency(self, database) : 

        """
        Retrieves the information according the website's given frequency
        """
            while True : 
                if self.computeMetrics(database, self.frequency)[1] : 
                    self.computeMetrics(database, self.frequency)
                else : 
                    print('No information available')
                time.sleep(self.frequency)



    def getInfo10min(self, database) :

        """
        Retrieves the information of the last 10min
        """

        while True : 
            if self.computeMetrics(database, 600)[1] : 
                self.computeMetrics(database, 600)
            else : 
                print('No information available')
            time.sleep(10)



    def getInfo60min(self, database) : 

        """
        Retrieves the information of the last 60min
        """

        while True : 
            if self.computeMetrics(database, 3600)[1] : 
                self.computeMetrics(database, 3600)
            else : 
                print('No information available')
            time.sleep(60)
