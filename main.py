import discord
import logging
from dotenv import load_dotenv
import os
from classes.Diary import Diary
from classes.User import User
import datetime
from datetime import timedelta
import re

load_dotenv()
token=os.getenv("TEST_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True

#group 1 = diary type, w(orkout)/f(ood). group 2 = name, group 3 = calories, 
#group 4 = specified date (mm-dd), group 5 = yesterday
reg_match_all = '(?:!)([w|f])\s*,\s*(\w+)\s*,\s*(-?\d+)\s*,?\s*(\d{1,2}\-\d{1,2})?\s*(y)?'



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
    if message.author == client.user:
        return

    #TODO add diary entry
    if re.match(reg_match_all,message.content):
        m = re.match(reg_match_all, message.content)
        print(m.groups())
        #group 1
        item_type=None
        if m.group(1)=='w':
            item_type = "Workout"
        if m.group(2)=='f':
            item_type = "Food"
        #group 2
        item_name = m.group(2)
        #group 3
        calories = m.group(3)
        #group 4/5    
        placeholder_date = datetime.date.today()
        if m.group(5) is not None: 
            print(datetime.date.today()- timedelta(days = 1))
            placeholder_date = datetime.date.today()-timedelta(days =1)
        if m.group(4) is not None:
            split = m.group(4).split("-")
            print(datetime.date(2023, int(split[0]), int(split[1])))
            placeholder_date = datetime.date(2023, int(split[0]), int(split[1]))

        diary_entry = Diary(message.author.id,placeholder_date,item_name,item_type,calories)
        print(diary_entry)

    else: print("doesn't match")

    #TODO: add view diary (only by id)
    
    #TODO: remove entry (by entry id)

    #TODO: clear by day

    #TODO: DELETE ALL

    #TODO: !help


    #print("text received")
    #print(message.author)
    #print(message.author.id)

    #Fun stuff
    if message.content.startswith('RAT ME'):
        await message.channel.send('<:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851>')
        await message.channel.send('RATTING YOU UP SUPER STYLE')
        await message.channel.send('<:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851>')
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

client.run(token, log_handler=handler)