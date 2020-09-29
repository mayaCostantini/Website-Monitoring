import monitoredWebsite
import threading
import requests 
from time import sleep 
import sqlite3
import HTTPSwitcher
from databaseManagement import createDatabase, createTable, dropTable, retrieveData

class monitor : 

    def __init__(self, databaseName) : 

        """
        Attributes : 
        - websitesList : editable list of the websites entered by the user (list)
        -  databaseName : name of the database where the metrics are stored (string)
        """

        self.websitesList = []
        self.database = databaseName

    def addWebsite(self, website) : 

        """
        Allows the user to add a website to the list websitesList
        """

        self.websitesList.append(website)

    def deleteWebsite(self, website) : 

        """
        Deletes a website from the list 
        """

        self.websitesList.remove(website)


    def initializeMonitor(self) : 

        """
        Cleans and initializes the database and table if necessary
        """
        
        dropTable('WebsitesData')
        createDatabase(self.database)
        createTable('WebsitesData')
