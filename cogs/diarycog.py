import datetime
import re
import discord
import datetime
from datetime import timedelta
import modules.dbservice as Dbservice
from modules.user import User
from modules.diary import Diary
import time
from tabulate import tabulate
import csv
import os

from discord.ext import commands

#group 1 = diary type, w(orkout)/f(ood). group 2 = name, group 3 = calories, 
#group 4 = specified date (mm-dd), group 5 = yesterday
#potential issue with dates being incorrect (ex 32 entered as month). Need to fix
reg_match_add = '(?:!)([w|W|f|F]|food|workout)\s+([\w|\s]+)\s*,\s*(-?\d+)\s*,?\s*(\d{1,2}\-\d{1,2})?\s*(y)?'
#group 1 = all, #group2 specific date, #group3 = yesterday, #group 4 = month #group 5 = csv
reg_match_view = "![v|V]iew(all)?\s*(\d{1,2}\-\d{1,2})?\s*(y)?(\d{1,2})?\s*(csv)?"

def makecsv(rows,userid):
    filestring = f"tempfiles/temp{userid}.csv"
    myfile = open(filestring,'w',newline='')
    writer = csv.writer(myfile)
    writer.writerow(['Entry','Date','Type','Item','Calories'])
    writer.writerows(rows)
    myfile.close()
    return filestring

#TODO: avg sum for larger time periods
class Diarycog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    #Add a diary entry
    @commands.command(aliases=['f','w','W','F','workout'])
    async def food(self, ctx):
        try:
            if re.match(reg_match_add,ctx.message.content):
                m = re.match(reg_match_add, ctx.message.content)
                #group 1
                item_type=None
                if m.group(1) in {'w','W','workout'}:
                    item_type = "Workout"
                if m.group(1) in {'f','F','food'}:
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
                diary_entry = Diary(ctx.message.author.id,placeholder_date,item_name,item_type,calories)
                Dbservice.add_diary(diary_entry)
                utctime=int(time.mktime(diary_entry.diarydate.timetuple()))
                await ctx.message.channel.send(f"<t:{utctime}:D> {diary_entry.entryname} for {diary_entry.calories} calories entered")
            else:
                await ctx.message.channel.send(f"I was unable to make out your request. Please follow the format found in !help")
        except:
            await ctx.message.channel.send("I came accross an error and could not process this request. Please make sure you have added yourself as a user with !add me")

    #View diary entry, with different options parsed
    @commands.command(aliases=['viewall'])
    async def view(self, ctx):
        try:
            if re.match(reg_match_view,ctx.message.content):
                m = re.match(reg_match_view, ctx.message.content)
                #Parse regex groups and use appropriate query to get diary entries. 
                if m.group(1) is not None:
                    entries = Dbservice.view_all(ctx.message.author.id)
                elif m.group(2) is not None:
                    split = m.group(2).split("-")
                    placeholder_date = datetime.datetime(2023, int(split[0]), int(split[1]))
                    entries = Dbservice.view_day(ctx.message.author.id,day=placeholder_date)
                elif m.group(3) is not None:
                    yesterday = datetime.datetime.today()-timedelta(days =1)
                    entries = Dbservice.view_day(ctx.message.author.id,day=yesterday)
                elif m.group(4) is not None:
                    entries = Dbservice.view_month(userid=ctx.message.author.id, month=int(m.group(4)))
                else: 
                    entries = Dbservice.view_day(ctx.message.author.id,datetime.datetime.today())
                #Parsing for query commands done, send file or text of results. 
                if m.group(5) is not None:
                    entries_file = makecsv(entries,ctx.message.author.id)
                    await ctx.message.channel.send(file=discord.File(entries_file))
                    os.remove(entries_file)
                elif len(entries)>99:
                    await ctx.message.channel.send("Volume is too large, please specify csv function instead to get a file")
                else:
                    mylist=[]
                    rowlimit = 10
                    #index 0 for food, index 1 for working out
                    sum=[0,0]
                    for i in range(len(entries)):
                        if (i)%rowlimit==0 and i!=0 :
                            await ctx.message.channel.send("```\n"+tabulate(mylist,headers=["Entry","Date","Type","Item","Cal"], tablefmt="grid")+"```") 
                            mylist.clear()
                        if(entries[i][2]=='Food'):
                            sum[0] += entries[i][4]
                        else:
                            sum[1] += entries[i][4] 
                        mylist.append(entries[i])
                    await ctx.message.channel.send("```\n"+ tabulate(mylist,headers=["Entry","Date","Type","Item","Cal"], tablefmt="grid")+"```") 
                    await ctx.message.channel.send(f"```Calories Consumed: {sum[0]}    |    Caloried Burned: {sum[1]}```") 
            else:
                await ctx.message.channel.send(f"I was unable to make out your request. Please follow the format found in !help")
        except:
            await ctx.message.channel.send("I came accross an error and could not process this request. Please make sure you have added yourself as a user with !add me")

    #Remove a diary entry
    @commands.command(aliases=['r','R'])
    async def remove(self, ctx):
        try:
            if re.match("!r\s+\d+",ctx.message.content):
                m = re.match("!r\s+(\d+)", ctx.message.content)
                removed_entry = Dbservice.remove_entry(m.group(1),ctx.message.author.id)
                if removed_entry is None:
                    await ctx.message.channel.send(f"entry {m.group(1)} could not be deleted. Either this entry Number does not exist or this is not your entry.")
                else:
                    await ctx.message.channel.send(f"``Entry No {removed_entry.id} deleted:``\n{removed_entry.diarydate} {removed_entry.entryname} for {removed_entry.calories} calories")
        except:
            await ctx.message.channel.send("I came accross an error and could not process this request.")