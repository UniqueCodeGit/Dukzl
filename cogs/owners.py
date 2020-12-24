import discord
import asyncio
from discord.ext import commands
from utils.general import GenerelUtils

class Owners(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot

    @commands.command(name = "리로드", aliases = ["reload"])
    @commands.is_owner()
    async def reload_cogs (self, ctx):
        GenerelUtils.AutoCommandsReload(self.bot)
        await ctx.send ("Reload Complete")


def setup (bot):
    bot.add_cog(Owners(bot))