import discord
import logging
import datetime
from utils.danny.dataIO import dataIO
from discord.ext import commands

desc = "uchuubranko; cXZmcGJlcXZuYQ0K; Discordian;"

maincolor = 0xF4601A  # defines the bots favorite color.

errorcolor = 0xFF3232
bot = commands.Bot(command_prefix="`", description=desc)

# set up logging as detailed in 1.0.0a docs
logger = logging.getLogger('discord')

logger.setLevel(logging.WARNING)

handler = logging.FileHandler(
    filename='log\discord.log', encoding='utf-8', mode='w')

handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

logger.addHandler(handler)

extlist = ["admin"]

def __init__():
    userinfo = dataIO.load_json("storage/userinf.json")


@bot.event
async def on_ready():
    loadExt()

    user = bot.get_user(oid)
    # gets current time and pms the owner.
    await user.send("Bot starting at `{} UTC -6`".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    print("Bot starting at {} UTC -6".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    print("Connected to Discord's API.")
    print(bot.user.name)
    print("Currently in {} servers".format(len(bot.guilds)))
    member_count = str(len([x for x in bot.get_all_members()]))
    print("I am in contact with " + member_count + " members.")

@bot.command(hidden=True,name="exit")
async def exitb(ctx):
    if ctx.author.id != oid:
        return
    print("Shutdown request by {}".format(ctx.author.name))
    bot.logout()
    exit()

@bot.command(hidden=True)
async def rel(ctx, module):
    if ctx.author.id != oid:
        return
    try:
        bot.unload_extension("ext." + module)
        bot.load_extension("ext." + module)
    except Exception as e:
        await ctx.send("An error has occured in reloading {}. Error : {}".format(module,e))
    finally:
        await ctx.send("Reloaded module {} correctly.".format(module))

@bot.command()
async def ping(ctx):
    # sends an embed "recieved."
    await ctx.send(embed=discord.Embed(title="Pong!", description="Recieved.", color=maincolor))


@bot.command()
async def info(ctx):
    await ctx.send(embed=discord.Embed(title="Bot Information", description="I am Stunning Image, a bot with many functions.\nI was created by cXZmcGJlcXZuYQ0K and Discordian.\nThank you.", color=maincolor))
    # general bot Information


@bot.command()
async def invite(ctx):
    await ctx.send("Thank you for wanting to invite to your server! {}".format(discord.utils.oauth_url(bot.user.id)))
    # creates an invite and sends it


def getUserInf():
    return userinfo

def loadExt():
    for ext in extlist:
        try:
            bot.load_extension("ext." + ext)
            print("Loaded ext {} correctly.".format(ext))
        except Exception as e:
            print("Unable to load extension {} due to error: {}".format(ext,e))
       
token = dataIO.load_json("storage/userinf.json")["token"]
oid = dataIO.load_json("storage/userinf.json")["id"]
bot.run(token)
