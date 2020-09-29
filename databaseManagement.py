import time 


def createDatabase(database) : 

    """
    Creates a database
    """

    conn = None 
    try : 
        conn = sqlite3.connect(database, timeout=100)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def createTable(database) : 

    """
    Creates the 'WebsitesData' database
    """

    conn = sqlite3.connect(database, timeout=100)
    c = conn.cursor()

    sqlite3.register_adapter(bool, int)
    sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))
   
    c.execute('CREATE TABLE IF NOT EXISTS WebsitesData (url VARCHAR(100), availability BOOLEAN, statusCode INT, responseTime FLOAT, date TEXT)')
    conn.commit()
    conn.close()
    return 

def dropTable(database) : 

    """
    Drops the 'WebsitesData' table if needed
    """

    conn = sqlite3.connect(database, timeout=100)
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS WebsitesData')

    conn.commit()
    conn.close()

def insertData(database, url, availability, statusCode, responseTime) :

    """
    Inserts data into the database
    """

    conn = sqlite3.connect(database, timeout=100)
    c = conn.cursor()

    date = datetime.now()
    values = (url, availability, statusCode, responseTime, date)
    c.execute('INSERT INTO WebsitesData (url, availability, statusCode, responseTime, date) VALUES (?, ?, ?, ?, ?) ', values)
    conn.commit()
    conn.close()
    
    return 

def retrieveData(database, url, date) : 

    """
    Selects data from the database
    """

    conn = sqlite3.connect(database, timeout=100)
    c = conn.cursor()

    values = (str(date), url)
    c.execute('SELECT availability, statusCode, responseTime FROM WebsitesData WHERE date <= ? AND url = ?', values)

    return c.fetchall()
