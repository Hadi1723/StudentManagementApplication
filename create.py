import sqlite3

#Connecting to sqlite
conn = sqlite3.connect('database/projectDatabase.db')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Doping EMPLOYEE table if already exists.
cursor.execute("DROP TABLE IF EXISTS STUDENTS")
#Doping EMPLOYEE table if already exists.
cursor.execute("DROP TABLE IF EXISTS CONTACTS")

#Creating table as per requirement
sql ='''CREATE TABLE STUDENTS(
   ID integer auto_increment primary key,
   FIRST_NAME CHAR(20) NOT NULL,
   LAST_NAME CHAR(20) NOT NULL,
   MACID CHAR(10) UNIQUE NOT NULL,
   GENDER CHAR(5) NOT NULL
)'''
cursor.execute(sql)
print("Student Table created successfully........")

#Creating table as per requirement
sql ='''CREATE TABLE CONTACTS(
   ID integer auto_increment primary key,
   MACID CHAR(10) UNIQUE NOT NULL,
   EMAIL CHAR(50) NOT NULL
)'''
cursor.execute(sql)
print("Contacts Table created successfully........")

# Commit your changes in the database
conn.commit()

#Closing the connection
conn.close()