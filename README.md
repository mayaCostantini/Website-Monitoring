# Websites Availability and Performance Monitoring CLI program


• Requirements

This program was written on a MacOS environment and needs Python3 and pip3 to be downloaded before proceeding to the installation of all the libraries listed below.
The commands to be then entered in the terminal are :
- pip3 install regex
- pip3 install requests - pip3 install threading - pip3 install datetime - pip3 install time
- pip3 install sqlite3
The program should be run in a console using the python3 interface.py command; the user’s menu should then be displayed.

• Classes

Here is the list of the different classes which were used to program this Website availability & Performance Monitoring interface.

Class monitoredWebsites : 

• Attributes :
- url : url of the website (string)
- frequency : interval in seconds at which the website will be checked (int) - status : current status for connection (bool)
- statusCode : current HTTP connection code

• Methods :
- urlFormat() : Inspects if the url attribute verifies the HTTP norms
- isAvailable() : Prints the connection status and the corresponding response code, returns True if
the connection is successful, False otherwise, returns the connection status, returns the
corresponding code for the connection status
- getResponseTime() : Computes the response time of the website in seconds
- getCurrentInfo() : returns a tuple with real-time information about the website’s availability
- sendInfo() : Sends current information to the database according to the ‘frequency’ attribute of the
class
- computeMetrics() : Computes the statistics
- getInfoWebsiteFrequency() : Retrieves the information according to the website’s frequency - getInfo10min() : Retrieves the information of the last 10min
- getInfo60min() : Retrieves the information of the last 60min

Class monitor : 

• Attributes :
- websitesList : list of the monitored websites (list) - databaseName : name of the database (string)

• Methods :
- addWebsite() : Adds a website to the list
- deleteWebsite() : Deletes a website from the list
- initializeMonitor() : Cleans and initialises the database and table if necessary

Class HTTPSwitcher : 

• Attributes :

- request : request send to the server of the website (attribute of the request class) - status_codes : associates the HTTP response codes to their meaning (hashmap)

• Methods :

- status() : Returns a string which describes the connection status in the status_codes hashmap and
the corresponding response code

The databaseManagement.py file provides function to manage the insertion and retrieval of data in the database.

• Improvement of the application design

This application design could be improved in several ways, which include :
- Display the statistics on a more “user-friendly” window, with text zones and buttons to click instead of commands to enter in the terminal
- Providing graphs to follow the availability rate of each website
- Allow users to check a website’s availability at all times and not only at a predefined frequency
- Compute statistics about the alert messages rates for a website in order to have a broader vision about its availability in a long term
