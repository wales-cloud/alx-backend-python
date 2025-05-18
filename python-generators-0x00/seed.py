import mysql.connector
import csv
import uuid

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password"
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()
    cursor.close()

def connect_to_prodev():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Thegoodlife_1",
            database="ALX_prodev"
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
        )
    """)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")

def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("SELECT COUNT(*) FROM user_data WHERE user_id = %s", (row['user_id'],))
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (row['user_id'], row['name'], row['email'], row['age'])
                )
    connection.commit()
    cursor.close()
