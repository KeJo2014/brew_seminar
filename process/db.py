import mysql.connector
from datetime import date
import asyncio

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="yourusername",
#   password="yourpassword"
# )


def create_new_table():
    # global mydb
    # mycursor = mydb.cursor()
    # mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
    table_name = 'Brauvorgang_'+date.today().strftime('%Y-%m-%d')
    print(f'created table called: {table_name}')


def insert_into_table(motor_mode, temperature):
    # mycursor = mydb.cursor()
    # sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
    # val = ("John", "Highway 21")
    # mycursor.execute(sql, val)
    # mydb.commit()
    # print(mycursor.rowcount, "record inserted.")
    print(
        f'Values successfullly inserted into table! ({temperature} // {motor_mode}')
