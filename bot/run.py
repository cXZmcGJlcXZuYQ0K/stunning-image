import discord
import logging
import aiohttp
import datetime
from utils.danny.dataIO import dataIO
from discord.ext import commands

desc = "uchuubranko; cXZmcGJlcXZuYQ0K; Discordian;"

bot = commands.Bot(command_prefix="`", description=desc)

oid = 108689770716069888
# set up logging as detailed in 1.0.0a docs
logger = logging.getLogger('discord')

logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(filename='log\discord.log', encoding='utf-8', mode='w')

handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

logger.addHandler(handler)


def __init__():
    userinfo = dataIO.load_json("storage/userinf.json")

@bot.event
async def on_ready():
    user = bot.get_user(oid)
    await user.send("Bot starting at `{}` UTC -6".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

token = dataIO.load_json("storage/userinf.json")["token"]
bot.run(token)
