import os
import sys 
import time
from monitor import monitor
from monitoredWebsite import monitoredWebsite
import databaseManagement
import threading 



def menu(Monitor) : 

    """
    User's menu to add, delete or monitor websites
    """
    
    choice = None
    while choice == None :
        print("\033[92m Website availability & performance monitoring project \033[0m")
        print("1 - Monitor websites")
        print("2 - Exit")

        choice = input("\t\t Enter a choice : ")

        if choice == "1":
            
            os.system('clear')
            choice = None 

            print("1 - See the list of current monitored websites")
            print("2 - Add a website to the list of monitored websites")
            print("3 - Delete a website from the list of monitored websites")
            print("4 - Begin monitoring")
            print("5 - Quit ")

            while choice == None : 

                choice = input("\t\t Enter a choice : ")

                if choice == "1" : 
                    os.system('clear')

                    newList = []
                    for website in Monitor.websitesList : 
                        newList.append(website.url)
                    print("Current Websites list : ", newList)

                    choice = None
                    break

                if choice == "2" : 
                    os.system('clear')
                    url = input("Enter the URL of the website to add : ")
                    frequency = int(input("Enter the checking frequency (in seconds) of the website to add : "))

                    Monitor.addWebsite(monitoredWebsite(url, frequency))

                    choice = None
                    break

                if choice == "3" : 
                    os.system('clear')
                    n = len(Monitor.websitesList)
                    url = input("Enter the URL of the website to delete : ")
                    for website in Monitor.websitesList : 
                        if website.url == url : 
                            Monitor.deleteWebsite(website)
                            print(f"Website {website.url} deleted ")
                    if n == len(Monitor.websitesList) : 
                        print("Website not found, please try again ")

                    choice = None
                    break 

                if choice == "4" : 
                    os.system('clear')

                    break 


        elif choice == "2":
            print('Thank you for using this program ')
            os._exit(0)

        else:
            print("I don't understand your choice.")
            menu(monitor)



def main() : 

    databaseManagement.createDatabase('test.db')
    databaseManagement.createTable('test.db')
    Monitor = monitor('test.db')
    menu(Monitor)

    Monitor.initializeMonitor()
    
    


    while True : 
        for website in Monitor.websitesList : 
            threading.Thread(target=monitoredWebsite.sendInfo, args=(website, 'test.db')).start()


            threading.Thread(target=monitoredWebsite.getInfoWebsiteFrequency, args=(website, 'test.db')).start()
            threading.Thread(target=monitoredWebsite.getInfo10min, args=(website,'test.db')).start()
            threading.Thread(target=monitoredWebsite.getInfo60min, args=(website, 'test.db')).start()
            
        time.sleep(10)


if __name__ == "__main__":
    main()
