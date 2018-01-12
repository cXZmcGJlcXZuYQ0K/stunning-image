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
            dataIO.save_json("storage/admin/datastruct.json", {})

    def isConfigured(self, ctx):
        if self.datastruct.get(str(ctx.guild.id)) is None:
            return False
        else:
            return True

    def isAdmin(self,ctx):
        if not self.isConfigured(ctx):
            if ctx.message.author.id == ctx.guild.owner.id:
                return True
            else:
                return False
        elif ctx.message.author.id in self.datastruct[str(ctx.guild.id)].get("modList") and "modifyServer" in self.datastruct[str(ctx.guild.id)].get("modList"):
            return True
        elif ctx.message.author.id == ctx.guild.owner.id:
            return True
        else:
            return False

    @commands.group()
    async def server(self, ctx):
        if not self.isAdmin(ctx):
            await ctx.send(embed=discord.Embed(color=main.errorcolor,title="Permissions Error",description="You do not have authority to do that in this server."))
        pass

    @server.group()
    async def welcome(self, ctx):
        if not await self.checkConfigured(ctx):
            return
        else:
            pass

    @commands.command()
    async def oxenwatch(self, ctx):
        oxenwatch = discord.utils.get(ctx.guild.roles, id=326858612737572865)
        try:
            if oxenwatch in ctx.author.roles:
                await ctx.author.remove_roles(oxenwatch)
                await ctx.send("You no longer have the Oxenwatch role.")
            else:
                await ctx.author.add_roles(oxenwatch)
                await ctx.send("You now have the Oxenwatch role.")
        except Exception as e:
            await ctx.send("I was unable to perform that action due to a permissions error.")

    @server.command()
    async def managemodpermissions(self, ctx):
        if not await self.checkConfigured(ctx):
            return
        else:
            return



    @welcome.command()
    async def message(self, ctx):
        """Changes what message is posted when a new user joins the server."""
        def check(m):
            return m.author.id == ctx.author.id
        if not await self.checkConfigured(ctx):
            return
        await ctx.send("Please specify the message you would like to change the welcome message to. To use special tags inside the message, insert a {name} into the message.")
        msg = await self.bot.wait_for('message', check=check)
        if msg is not None:
            if "{name}" in msg.content:
                modifiers = ["memberName"]
                self.datastruct[str(ctx.guild.id)]["wModifiers"] = modifiers
                msg = msg.content.replace("{name}", '{0.display_name}')
            self.datastruct[str(ctx.guild.id)]["wMessage"] = msg
            self.datastruct[str(ctx.guild.id)]["wToggle"] = True
            await ctx.send("Changed the welcome message to `{}`.".format(msg))
            dataIO.save_json("storage/admin/datastruct.json", self.datastruct)

    @welcome.command()
    async def channel(self, ctx):
        def check(m):
            return m.author.id == ctx.author.id
        if not await self.checkConfigured(ctx):
            return
        await ctx.send("Post the channel that you would like the messages to be posted in.")
        msg = await self.bot.wait_for('message', check=check)
        if msg.channel_mentions is not None:
            perms = msg.channel_mentions[0].permissions_for(ctx.guild.get_member(self.bot.user.id))
            if perms.send_messages is False:
                await ctx.send("I can not post messages in that channel. Aborting operation.")
            else:
                self.datastruct[str(ctx.guild.id)]["wChannel"] = msg.channel_mentions[0].id
                await ctx.send("Set welcome messages to post in the channel: {}".format(msg.channel_mentions[0].name))
    def canBan(self, ctx):
        if not self.isAdmin(ctx):
            return False
        if "banUsers" in self.datastruct[str(ctx.guild.id)].get("modPerms"):
            return True
        if ctx.guild.owner.id == ctx.author.id:
            return True
    async def permissionserror(self,ctx):
         await ctx.send(
             'You do not have the required permissions to perform this function.\n If this seems like an error, please let the server owner know.')

    @server.command(name="ban")
    async def banuser(self,ctx, user: discord.Member,*,reason=None):
        if not await self.checkConfigured(ctx):
            return
        if not self.canBan(ctx):
            await self.permissionerror(ctx)
            return
        if reason is not None:
            await ctx.guild.ban(user, reason=reason)
        else:
            await ctx.guild.ban(user, reason="Banned by {}".format(ctx.message.author.display_name))
        await ctx.guild.owner.send("I have just banned the user `{}`. This action was performed by `{}`.".format(user.display_name, ctx.message.author.display_name))



    async def checkConfigured(self, ctx):
        if not self.isConfigured(ctx):
            await ctx.send("You must configure this server. Do to that, run the command ``server configure`")
            return False
        else:
            return True

    @welcome.command()
    async def toggle(self, ctx):
        if not await self.checkConfigured(ctx):
            return
        """Changes whether or not the welcome message is used"""
        if self.datastruct[str(ctx.guild.id)].get("wToggle") is True:
            self.datastruct[str(ctx.guild.id)]["wToggle"] = False
            await ctx.send(embed=discord.Embed(title="Changed Settings!", description="I have turned off welcome messages for this server!", color=main.maincolor))
        else:
            await ctx.send(embed=discord.Embed(title="Changed Settings!", description="I have turned on welcome messages for this server!", color=main.maincolor))
            self.datastruct[str(ctx.guild.id)]["wToggle"] = True

    @server.command(name="mod")
    async def managemods(self, ctx, mod : discord.Member):
        """Adds a user to the moderator team, or removes a current moderator."""
        if not self.isConfigured(ctx):
            await ctx.send("You must configure this server. Do to that, run the command ``server configure`")
        else:
            if mod.id in self.datastruct[str(ctx.guild.id)]["modList"]:
                self.datastruct[str(ctx.guild.id)]["modList"].remove(mod.id)
                await ctx.send(embed=discord.Embed(title="Task Completed",description="I have removed {} as a moderator.".format(mod.display_name),color=main.maincolor))
                await mod.send("You have been removed as a moderator to {}".format(ctx.guild.name))
            else:
                self.datastruct[str(ctx.guild.id)]["modList"].append(mod.id)
                await ctx.send(embed=discord.Embed(title="Task Completed", description="I have added {} as a moderator.".format(mod.display_name), color=main.maincolor))
                await mod.send("You have been added as a moderator to {}".format(ctx.guild.name))

    @server.command()
    async def changeperms(self,ctx):
        """Changes what moderators can do. Must have Admin/Server Owner to use this command."""
        guild = ctx.guild
        if not self.isConfigured(ctx):
            return
        if not self.isAdmin(ctx):
            return
        else:
            await ctx.send(embed=discord.Embed(title="Server Configuration",
                                               description='Enter all attributes you want moderators to have access to.\n\n1. Modify Server Settings\n\n2. Restrict users from using the bot.\n\n3. Ban/Kick Users.'))
            def check(m):
                return m.author.id == ctx.author.id
            msg = await self.bot.wait_for('message', check=check)
            permlist = {"1": "modifyServer", "2": "whitelistUsers", "3": "banUsers"}
            addtolist = []
            for i in msg.content:
                addtolist.append(permlist[i])
            # dictTemp = {"modPerms": addtolist}
            self.datastruct[str(guild.id)] = {}
            self.datastruct[str(guild.id)]["modPerms"] = addtolist
            dataIO.save_json("storage/admin/datastruct.json", self.datastruct)
            await ctx.send("I have updated moderator permissions.")

    @server.command()
    async def configure(self, ctx):
        """Configures how the bot will work in this server. This is a must for all other commands in this category."""
        guild = ctx.guild
        # set up the data structure for the server.
        if self.isConfigured(ctx) is True:
            await ctx.send("This server is already configured. You may change your settings with ``server settings`")
            return
        else:
            await ctx.send(embed=discord.Embed(title="Server Configuration", description='Enter all attributes you want moderators to have access to.\n\n1. Modify Server Settings\n\n2. Restrict users from using the bot.\n\n3. Ban/Kick Users.'))
            def check(m):
                return m.author.id == ctx.author.id 
            msg = await self.bot.wait_for('message', check=check)
            permlist = {"1": "modifyServer", "2": "whitelistUsers", "3" : "banUsers"}
            addtolist = []
            for i in msg.content:
                addtolist.append(permlist[i])
           # dictTemp = {"modPerms": addtolist}
            self.datastruct[str(guild.id)] = {}
            self.datastruct[str(guild.id)]["modPerms"] = addtolist
            await ctx.send(embed=discord.Embed(title="Server Configuration",description="Mention all users that you want to add as moderators. Type `none` if you want none currently.",color=main.maincolor))
            msg = await self.bot.wait_for('message', check=check)
            add2 = []
            if "none" in msg.content:
                self.datastruct[str(guild.id)]["modList"] = []
            else:
                for mention in msg.mentions:
                    add2.append(mention.id)
                self.datastruct[str(guild.id)]["modList"] = add2
            dataIO.save_json("storage/admin/datastruct.json", self.datastruct)  
            await ctx.send(embed=discord.Embed(title="Configuration Complete!", description="Your server has been set up. use the command ``help server` for other subcommands.",color=main.maincolor))

    async def on_member_join(self, member):
        struct = self.datastruct[str(member.guild.id)]
        if self.isConfigured(member):
            if struct.get("wMessage") is not None:
                if struct["wToggle"]:
                    chan = self.bot.get_channel(struct.get("wChannel"))
                    if struct["wModifiers"] is not None:
                        tempstring = struct["wMessage"]
                        await chan.send(tempstring.format(member))
                    else:
                        await chan.send(struct["wMessage"])
                else:
                    pass
            else:
                pass
        else:
            pass
            


def setup(bot):
    bot.add_cog(Admin(bot))

