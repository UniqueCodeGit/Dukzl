from discord.ext import commands

from utils.general import GenerelUtils


class Owners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="리로드", aliases=["reload"])
    @commands.is_owner()
    async def reload_cogs(self, ctx):
        GenerelUtils.AutoCommandsReload(self.bot)
        await ctx.send("Reload Complete")

    @commands.command(name="언로드", aliases=["unload"])
    @commands.is_owner()
    async def unload_cogs(self, ctx):
        await ctx.send("ㄴ")

    @commands.command(name="로드", aliases=["load"])
    @commands.is_owner()
    async def load_cogs(self, ctx):
        GenerelUtils.AutoCommandsload(self.bot)
        await ctx.send("Load Complete")


def setup(bot):
    bot.add_cog(Owners(bot))
