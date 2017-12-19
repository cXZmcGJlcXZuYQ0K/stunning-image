import discord
from discord.ext import commands
import os 
import __main__ as main
from utils.danny.dataIO import dataIO


class Admin:
    def __init__(self, bot):
        self.bot = bot
        self.checkStructure()
        self.datastruct = dataIO.load_json("storage/admin/datastruct.json")


    def checkStructure(self):
        if not os.path.isdir("storage/admin"):
            os.mkdir("storage/admin")
        if not os.path.isfile("storage/admin/datastruct.json"):
            data = {}
            dataIO.save_json("storage/admin/datastruct.json", data)
    

    def isConfigured(self, sid):
        print(self.datastruct)
        if self.datastruct.get(sid) is not None:
            return True
        else:
            return False

    @commands.group()
    async def server(self, ctx):
        #if not isAdmin():
        #    await ctx.send(embed=discord.Embed(color=main.errorcolor,title="Permissions Error",description="You do not have authority to do that in this server."))
        pass

    @server.command()
    async def configure(self, ctx):
        guild = ctx.guild
        # set up the data structure for the server.
        if self.isConfigured(guild.id) is True:
            await ctx.send("This server is already configured. You may change your settings with ``server settings`")
        else:
            await ctx.send(embed=discord.Embed(title="Server Configuration",description="Enter all attributes you want moderators to have access to.\n\n1. Modify Server Settings\n\n2. Restrict users from using the bot."))
            def check(m):
                return m.author.id == ctx.author.id 
            msg = await self.bot.wait_for('message', check=check)
            permlist = {"1": "modifyServer", "2": "whitelistUsers"}
            addTolist = []
            for i in msg.content:
                addTolist.append(permlist[i])
            dictTemp = {"modPerms": addTolist}
            self.datastruct[guild.id] = {}
            self.datastruct[guild.id]["modPerms"] = addTolist
            await ctx.send(embed=discord.Embed(title="Server Configuration",description="Mention all users that you want to add as moderators.",color=main.maincolor))
            msg = await self.bot.wait_for('message', check=check)
            add2 = []
            for mention in msg.mentions:
                add2.append(mention.id)
            self.datastruct[guild.id]["modList"] = add2
            dataIO.save_json("storage/admin/datastruct.json", self.datastruct)  
            await ctx.send(embed=discord.Embed(title="Configuration Complete!", description="Your server has been set up. use the command ``help server` for other subcommands.",color=main.maincolor))
            


def setup(bot):
    bot.add_cog(Admin(bot))

