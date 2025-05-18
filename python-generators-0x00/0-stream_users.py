import mysql.connector

def stream_users():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Thegoodlife_1",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        cursor.close()
        connection.close()
