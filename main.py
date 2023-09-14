import discord
import logging
from dotenv import load_dotenv
import os
from cogs.usercog import Usercog
from cogs.ratcog import Ratcog
from discord.ext import commands
from cogs.diarycog import Diarycog


load_dotenv()
token=os.getenv("TEST_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot("!",intents=intents,help_command=None)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await setup(client)

async def setup(client):
    await client.add_cog(Ratcog(client))
    await client.add_cog(Usercog(client))
    await client.add_cog(Diarycog(client))
    @client.command()
    async def help(ctx):
        await ctx.message.channel.send("""\t\t\tDate is an optional specification for all commands. Format mm-dd\n\
It can be omitted to default to today, or 'y' can be used to indicate yesterday\n\n\
__CommandList:__\n\
Adding Food :  ``!f itemname,calories,date``\n\
Adding a Workout:  ``!w itemname,calories,date``\n\
Viewing Entries:  ``!view date``\n\
Removing Entry : ``!r entryeumber``\n\
**The entry you are trying to remove must belong to you. You can find the entry number when viewing.\n\n\
__Examples:__\n\
Adding a banana today: ``!f banana,105``\n\
Adding some cardio yesterday: ``!w running,200,y``\n\
Adding an icecream sandwich on Sept 8th: ``!f icecream sandwich,210,09-08``\n\
Viewing todays entries: ``!view``\n\
Viewing entries for all of September: ``!view 09``\n\
Viewing entries for September 9th: ``!view 09-09``\n\
Removing Entry number 8: ``!r 8``\n\n\
__Fun stuff:__\n\
RAT ME, rat me, jam me""")

#TODO: flesh out log handler for error catching & troubleshooting
client.run(token, log_handler=handler)