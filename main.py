import discord
import logging
from dotenv import load_dotenv
import os

load_dotenv()

token=os.getenv("TEST_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        newmessage = await message.channel.send('Hello!')
        await newmessage.add_reaction('1256rat:1109634304310517851')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('RAT ME'):
        newmessage = await message.channel.send('<:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851>')
        newmessage = await message.channel.send('RATTING YOU UP SUPER STYLE')
        newmessage = await message.channel.send('<:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851><:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851>')
        await message.add_reaction('1256rat:1109634304310517851')
        await message.add_reaction('a:ratjam:1147635795017076776')
    elif message.content.lower() == 'rat me':
        newmessage = await message.channel.send('RATTING YOU UP')
        newmessage = await message.channel.send('<:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851> <:1256rat:1109634304310517851>')
        await message.add_reaction('1256rat:1109634304310517851')
        #await newmessage.add_reaction('1256rat:1109634304310517851')
    elif message.content.lower() == 'jam me':
        newmessage = await message.channel.send('JAMMING YOU UP')
        newmessage = await message.channel.send('<a:ratjam:1147635795017076776><a:ratjam:1147635795017076776><a:ratjam:1147635795017076776><a:ratjam:1147635795017076776><a:ratjam:1147635795017076776>')
        await message.add_reaction('<a:ratjam:1147635795017076776>')
    

client.run(token, log_handler=handler)