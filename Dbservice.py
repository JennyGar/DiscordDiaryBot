from classes.User import User
from classes.Diary import Diary
import mysql.connector
from dotenv import load_dotenv
import datetime
import os

load_dotenv()
dbpass=os.getenv("DB_PASS")

def connect()->mysql.connector:
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  database="mydb",
  password=dbpass  
  )
  return mydb

#Adds diary entry to table
def add_diary(diary: Diary):
  mydb = connect()
  mycursor = mydb.cursor(buffered=True)
  sql = "INSERT INTO diary(Userid, Diarydate, Entrytype, Entryname, Calories) VALUES (%s, %s, %s, %s, %s)"
  val = (diary.userID, diary.diarydate.strftime('%Y-%m-%d %H:%M:%S'), diary.entrytype, diary.entryname, diary.calories)
  mycursor.execute(sql, val)
  mydb.commit()
  mycursor.close()
  mydb.close()

d1 = Diary(128342056262303744, diarydate=datetime.datetime.now(), entrytype = 'food', entryname='banana', calories = 120)
add_diary(d1)




""" mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  database="mydb",
  password=dbpass
)

print(mydb) 

mycursor = mydb.cursor(buffered=True)
mycursor.execute("SHOW TABLES")
for x in mycursor:
    print(x)

sql = "INSERT INTO diary(Userid, Diarydate, Entrytype, Entryname, Calories) VALUES (%s, %s, %s, %s, %s)"
val = (128342056262303744, d1.diarydate.strftime('%Y-%m-%d %H:%M:%S'), d1.entrytype, d1.entryname, d1.calories)

mycursor.execute(sql, val)
mydb.commit() """