##THIS IS A TESTFILE TO TRY OUT INDIVIDUAL FUNCTIONS. USE IT HOWEVER YOU WANT. 


import mysql.connector
from dotenv import load_dotenv
from classes.Diary import Diary
from classes.User import User
import datetime
import os
import re
import Dbservice
import time
from tabulate import tabulate


entries = Dbservice.view_day(128342056262303744,datetime.datetime.today())

#print(tabulate(entries,headers=["Entry","Date","Type","Item","Calories"], tablefmt="grid"))

#if len > 100 too much
#else loop through, every x print await then clear lsit and start again
mylist=[]
limit = 2 
sum = 0
for i in range(len(entries)):
    if (i)%limit==0 and i!=0 :
       print(tabulate(mylist,headers=["Entry","Date","Type","Item","Calories"], tablefmt="grid")) 
       mylist.clear()
    mylist.append(entries[i])
    if(entries[i][2]=='Food'):
        sum += entries[i][4]
    else:
        sum -= entries[i][4] 
if len(entries)%limit!=0:
    print(tabulate(mylist,headers=["Entry","Date","Type","Item","Calories"], tablefmt="grid")) 

print(f"total:{sum}")

""" mylist.append(entries[0])
mylist.append(entries[1])
mylist.append(entries[2])
mylist.append(entries[3]) """



#str = (tabulate(mylist,headers=["Entry","Date","Type","Item","Calories"], tablefmt="grid"))
#print(str)



""" a = 1
a += 2
print(a) 
print("location: {0:20} Revision: {0:20} a".format("location", "revision")) """
#print(datetime.datetime.today())
#mytime = time.mktime(datetime.datetime.today().timetuple())
#print(int(mytime))

#utctime=int(time.mktime(datetime.diarydate.date.timetuple()))

#d1 = Diary(128342056262303744, diarydate=datetime.date.today(), entrytype = 'Food', entryname='Newfood', calories = 520)
#print(d1)
#Dbservice.add_diary(d1)



""" print(datetime.date(2023,9,15))

mystring = '!w,cardio,200'
ex2 = '!f,as'

regmatchdate  = '(?:!)([w|f])\s*,\s*(\w+)\s*,\s*(\d+)\s*,\s*(\d{1,2}\-\d{1,2})\s*'
regmatchy = '(?:!)([w|f])\s*,\s*(\w+)\s*,\s*(\d+)\s*,\s*(y)\s*'
regmatch = '(?:!)([w|f])\s*,\s*(\w+)\s*,\s*(\d+)\s*'
regmatchall = '(?:!)([w|f])\s*,\s*(\w+)\s*,\s*(\d+)\s*,?\s*(\d{1,2}\-\d{1,2})?\s*(y)?'
#Group 4 is date, Group 5 is yesterday

d1 = Diary(userid=1234, diarydate=datetime.datetime.now(), entrytype = 'food', entryname='banana', calories = 120)
print(d1)
print(d1.diarydate.strftime('%Y-%m-%d %H:%M:%S'))

if re.match(regmatchall,ex2):
    print("yes")
else: print("no") """
""" m = re.match(regmatchall, ex2)
print(m.groups())
for i in range(1, len(m.groups())+1):
    print(m.group(i)) """

#DB stuff
""" load_dotenv()
dbpass=os.getenv("DB_PASS")

mydb = mysql.connector.connect(
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
mydb.commit()

 """