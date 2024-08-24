import mysql.connector
from mysql.connector import Error
db_name = 'fitness'
user = 'root'
password = '#Fuckshit26'
host = 'localhost' # local host = 127.0.0.1

def connection():
    '''
    Creates a database connection to fitness database
    '''
    try:
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )

        if conn.is_connected():
            print('Successfully connected to fitness database!')
            return conn
        
    except Error as e:
        print(f"Error: {e}")
        return None