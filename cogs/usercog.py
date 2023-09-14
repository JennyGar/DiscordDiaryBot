import discord
import classes.Dbservice as Dbservice
from classes.User import User
import time
import tabulate

from discord.ext import commands

#group 1 = all, #group2 specific date, #group3 = yesterday, #group 4 = month
reg_match_view = "![v|V]iew(all)?,?\s*(\d{1,2}\-\d{1,2})?\s*(y)?(\d{1,2})?"

class Usercog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self:
            return
        
        if message.content.lower()=="!add me":
            temp = Dbservice.add_user(message.author.id, str(message.author))
            if temp is None:
                await message.channel.send("You've already been added! Type ``!help`` for guidance on commands")
            elif temp == 1:
                await message.channel.send("You're username has been adjusted. Type ``!help`` for guidance on commands")
            else:
                await message.channel.send("You've been added! Type ``!help`` for guidance on commands")