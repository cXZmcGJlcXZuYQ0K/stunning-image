import discord
from discord.ext import commands
from utils.danny.dataIO import dataIO
import inspect


class Debug:

    def __init__(self, bot):
        self.bot = bot
        self.oid = dataIO.load_json("storage/userinf.json")["id"]

    @commands.command(hidden=True)
    async def py(self,ctx, *, code: str):
        """Evaluates code. -thanks danny"""
        code = code.strip('` ')
        python = '```py\n{}\n```'
        result = None
        if ctx.message.author.id == self.oid:
            pass
        else:
            return
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'guild': ctx.message.guild,
            'channel': ctx.message.channel,
            'author': ctx.message.author
        }
        env.update(globals())

        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await ctx.send(python.format(type(e).__name__ + ': ' + str(e)), delete_after=10)
            return
        await ctx.send(python.format(result), delete_after=10)


def setup(bot):
    bot.add_cog(Debug(bot))
