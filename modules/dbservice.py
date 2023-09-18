from modules.user import User
from modules.diary import Diary
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
  val = (diary.userID, diary.diarydate, diary.entrytype, diary.entryname, diary.calories)
  mycursor.execute(sql, val)
  mydb.commit()
  mycursor.close()
  mydb.close()

#Returns a truple of entries on a specific day for a specific user
def view_day(userid: int, day: datetime)->list:
  mydb = connect()
  mycursor = mydb.cursor()
  sql = "SELECT Diaryid, Diarydate, Entrytype, Entryname, Calories FROM diary WHERE Userid=%s AND Diarydate=%s"
  val = (userid,day.date())
  mycursor.execute(sql, val)
  myresult = mycursor.fetchall()
  mycursor.close()
  mydb.close()
  return myresult

#Returns a truple of all entries for a specific user
#TODO: sort default by date 
def view_all(userid: int)->list:
  mydb = connect()
  mycursor = mydb.cursor()
  sql = "SELECT Diaryid, Diarydate, Entrytype, Entryname, Calories FROM diary WHERE Userid=%(userid)s"
  mycursor.execute(sql, {'userid': userid})
  myresult = mycursor.fetchall()
  mycursor.close()
  mydb.close()
  return myresult

#Returns a truple of all entries in a specific month for a specific user
def view_month(userid: int, month: int):
  mydb = connect()
  mycursor = mydb.cursor()
  sql = "SELECT Diaryid, Diarydate, Entrytype, Entryname, Calories FROM diary WHERE Userid=%s AND MONTH(diarydate) =%s"
  val = (userid,month)
  mycursor.execute(sql,val)
  myresult = mycursor.fetchall()
  mycursor.close()
  mydb.close()
  return myresult

#remove entry by diary id. User id provided to ensure match. 
def remove_entry(diaryid: int,userid: int)->list:
  mydb = connect()
  mycursor = mydb.cursor()
  #Geting info on entry and verifying user before deleting it
  sql = "SELECT Diaryid, Userid, Diarydate, Entrytype, Entryname, Calories FROM diary WHERE Diaryid=%(diaryid)s"
  mycursor.execute(sql, {'diaryid': diaryid})
  entry = mycursor.fetchone()
  if entry is None:
    return None
  elif entry[1]!= userid:
    return None
  sql = "DELETE FROM diary WHERE Diaryid=%(diaryid)s"
  mycursor.execute(sql, {'diaryid': diaryid})
  mydb.commit()
  mycursor.close()
  mydb.close()
  diary = Diary(userid=entry[1], diarydate=entry[2],entryname=entry[4],entrytype=entry[3],calories=entry[5])
  diary.id=entry[0]
  return diary

#returns userid if added, returns 1 if username adjusted, returns None if no adjustments
def add_user(userid: int, username:str)->int:
  mydb = connect()
  mycursor = mydb.cursor(buffered=True)
  sql = "SELECT Userid,Username FROM user WHERE Userid=%(userid)s"
  mycursor.execute(sql, {'userid' : userid})
  entry = mycursor.fetchone()
  if entry is None:
    sql = "INSERT INTO user(Userid, Username) VALUES (%s, %s)"
    val = (userid,username)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()
    mydb.close()
    return userid
  elif entry[1]!=username:
    sql = "UPDATE user SET Username=%s WHERE Userid=%s"
    val = (username,userid)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()
    mydb.close()
    return 1
  else:
    return None
  