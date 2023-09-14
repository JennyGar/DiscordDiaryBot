import datetime
import re
import discord
import datetime
from datetime import timedelta
import classes.Dbservice as Dbservice
from classes.User import User
from classes.Diary import Diary
import time
import tabulate

from discord.ext import commands

class Ratcog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

#example for future use of command.
    @commands.command(aliases=['ratata'])
    async def rat_me(self,ctx):
        await ctx.message.channel.send("aaa")
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self:
            return
        if message.content.startswith('RAT ME'):
            await message.channel.send('<:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851>')
            await message.channel.send('RATTING YOU UP SUPER STYLE')
            await message.channel.send('<:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851>')
            ##I have sticker id, but haven't figured out how to send it yet. 
            mysticker = sticker=self.get_sticker(1148747539131146370)
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