import mysql.connector




def connect_db():
    try:
        cnx = mysql.connector.connect(
            host = 'your ip',
            port = 3306,
            database = 'budget_tracker',
            user = 'your user',
            password = 'your pwd'
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return -1
    else:
        return cnx
    

def insert_query(query):
    try:
        cnx = connect_db()
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        return 1
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return -1
    
def select_query(query):
    try:
        cnx = connect_db()
        cursor = cnx.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return -1