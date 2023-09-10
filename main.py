import discord
import logging
from dotenv import load_dotenv
import os
from classes.Diary import Diary
from classes.User import User
import datetime
from datetime import timedelta
import re
import Dbservice
import time
from tabulate import tabulate


load_dotenv()
token=os.getenv("TEST_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True

#group 1 = diary type, w(orkout)/f(ood). group 2 = name, group 3 = calories, 
#group 4 = specified date (mm-dd), group 5 = yesterday
#potential issue with dates being incorrect (ex 32 entered as month)
reg_match_all = '(?:!)([w|W|f|F])\s*,\s*([\w|\s]+)\s*,\s*(-?\d+)\s*,?\s*(\d{1,2}\-\d{1,2})?\s*(y)?'
#group 1 = all, #group2 specific date, #group3 = yesterday, #group 4 = month
reg_match_view = "![v|V]iew(all)?,?\s*(\d{1,2}\-\d{1,2})?\s*(y)?(\d{1,2})?"



client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


##bots reaction to its own message
@client.event
async def on_message(message):
    if message.author == client.user:
        return

#bots reaction to messages not by self
@client.event
async def on_message(message):
    try:
        if message.author == client.user:
            return
        
        if message.content.lower()=="!add me":
            temp = Dbservice.add_user(message.author.id, str(message.author))
            if temp is None:
                await message.channel.send("You've already been added! Type ``!help`` for guidance on commands")
            elif temp == 1:
                await message.channel.send("You're username has been adjusted. Type ``!help`` for guidance on commands")
            else:
                await message.channel.send("You've been added! Type ``!help`` for guidance on commands")

        #add diary entry
        #TODO add response
        if re.match(reg_match_all,message.content):
            m = re.match(reg_match_all, message.content)
            #group 1
            item_type=None
            if m.group(1)=='w':
                item_type = "Workout"
            if m.group(1)=='f':
                item_type = "Food"
            #group 2
            item_name = m.group(2)
            #group 3
            calories = abs(int(m.group(3)))
            #group 4/5    
            placeholder_date = datetime.date.today()
            if m.group(5) is not None: 
                placeholder_date = datetime.date.today()-timedelta(days =1)
            if m.group(4) is not None:
                split = m.group(4).split("-")
                placeholder_date = datetime.date(2023, int(split[0]), int(split[1]))
            diary_entry = Diary(message.author.id,placeholder_date,item_name,item_type,calories)
            Dbservice.add_diary(diary_entry)
            utctime=int(time.mktime(diary_entry.diarydate.timetuple()))
            await message.channel.send(f"<t:{utctime}:D> {diary_entry.entryname} for {diary_entry.calories} calories entered")

        ##view by day
        ##TODO: Make mobile view easier. Adjust year before it becomes an issue
        ##TODO: Add csv option
        elif re.match(reg_match_view,message.content):
            m = re.match(reg_match_view, message.content)
            if m.group(1) is not None:
                entries = Dbservice.view_all(message.author.id)
            elif m.group(2) is not None:
                split = m.group(2).split("-")
                placeholder_date = datetime.datetime(2023, int(split[0]), int(split[1]))
                entries = Dbservice.view_day(message.author.id,day=placeholder_date)
            elif m.group(3) is not None:
                yesterday = datetime.datetime.today()-timedelta(days =1)
                entries = Dbservice.view_day(message.author.id,day=yesterday)
            elif m.group(4) is not None:
                entries = Dbservice.view_month(userid=message.author.id, month=int(m.group(4)))
            else: 
                entries = Dbservice.view_day(message.author.id,datetime.datetime.today())
            if len(entries)>99:
                await message.channel.send("Due to the volume I won't be posting, but will instead offer a csv. Please stay tuned for csv option to be added")
            else:
                mylist=[]
                rowlimit = 10
                #index 0 for food, index 1 for working out, index 2 for less 
                sum=[0,0,0]
                for i in range(len(entries)):
                    if (i)%rowlimit==0 and i!=0 :
                        await message.channel.send("```\n"+tabulate(mylist,headers=["Entry","Date","Type","Item","Cal"], tablefmt="grid")+"```") 
                        mylist.clear()
                    if(entries[i][2]=='Food'):
                        sum[0] += entries[i][4]
                    else:
                        sum[1] += entries[i][4] 
                    mylist.append(entries[i])
                await message.channel.send("```\n"+ tabulate(mylist,headers=["Entry","Date","Type","Item","Cal"], tablefmt="grid")+"```") 
                await message.channel.send(f"```Calories Consumed: {sum[0]}    |    Caloried Burned: {sum[1]}```")
            
        #remove entry
        elif re.match("!r,\d+",message.content):
            m = re.match("!r,(\d+)", message.content)
            removed_entry = Dbservice.remove_entry(m.group(1),message.author.id)
            if removed_entry is None:
                await message.channel.send(f"entry {m.group(1)} could not be deleted. Either this entry Number does not exist or this is not your entry.")
            else:
                await message.channel.send(f"``Entry No {removed_entry.id} deleted:``\n{removed_entry.diarydate} {removed_entry.entryname} for {removed_entry.calories} calories")

        #TODO: clear by day

        #TODO: DELETE ALL

        #!help option. Should probably just move this to a txt file. Maybe change to an embed
        elif message.content.lower()==('!help'):
            await message.channel.send("""\t\t\tDate is an optional specification for all commands. Format mm-dd\n\
It can be omitted to default to today, or 'y' can be used to indicate yesterday\n\n\
__CommandList:__\n\
Adding Food :  ``!f,itemname,calories,date``\n\
Adding a Workout:  ``!w,itemname,calories,date``\n\
Viewing Entries:  ``!view,date``\n\
Removing Entry : ``!r,entryeumber``\n\
**The entry you are trying to remove must belong to you. You can find the entry number when viewing.\n\n\
__Examples:__\n\
Adding a banana today: ``!f,banana,105``\n\
Adding some cardio yesterday: ``!w,running,200,y``\n\
Adding an icecream sandwich on Sept 8th: ``!f,icecream sandwich,210,09-08``\n\
Viewing todays entries: ``!view``\n\
Viewing entries for all of September: ``!view,09``\n\
Viewing entries for September 9th: ``!view,09-09``\n\
Removing Entry number 8: ``!r,8``\n\n\
__Fun stuff:__\n\
RAT ME, rat me, jam me""")

        #Fun stuff
        elif message.content.startswith('RAT ME'):
            await message.channel.send('<:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851>')
            await message.channel.send('RATTING YOU UP SUPER STYLE')
            await message.channel.send('<:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851>')
            ##I have sticker id, but haven't figured out how to send it yet. 
            mysticker = sticker=client.get_sticker(1148747539131146370)
            print(mysticker.name)
            await message.add_reaction('1256rat:1109634304310517851')
            await message.add_reaction('a:ratjam:1147635795017076776')
        elif message.content.lower() == 'rat me':
            await message.channel.send('RATTING YOU UP')
            await message.channel.send('<:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851>')
            await message.add_reaction('1256rat:1109634304310517851')
        elif message.content.lower() == 'jam me':
            await message.channel.send('JAMMING YOU UP')
            newmessage = await message.channel.send('<a:ratjam:1147635795017076776><a:ratjam:1147635795017076776><a:ratjam:1147635795017076776><a:ratjam:1147635795017076776><a:ratjam:1147635795017076776>')
            await message.add_reaction('<a:ratjam:1147635795017076776>')
    except:
        try:
            await message.channel.send("I came across an error and could not process this request.\n\
•  Please make sure you have added yourself with the ``!add me`` command\n\
•  Type ``!help`` to see text options\n\
•  Contact zaphiraf on Discord if you have any further questions or suggestions")
        except:
            print("error experienced")

client.run(token, log_handler=handler)