import os
import discord
import discodo
from discord.ext import commands
from .utils.log import Log


class Dukzl(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=["$"],
            help_command=None,
            activity=discord.Game("$도움 | Dukzl 1.0"),
            intents=discord.Intents.all(),
        )
        self.logger = Log.cogLogger(self)
        self.discordLogger = Log.discordLogger()
        self.Wonstein = discodo.DPYClient(self)

    async def on_ready(self):
        self.logger.info(f"Dukzl loaded as {self.user.name}")


def auto_load_cogs(bot: Dukzl):
    cmdlist = os.listdir("Dukzl/cogs/")

    for i in cmdlist:
        if i.endswith(".py") and not i.startswith("__"):
            cmdname = f"Dukzl.cogs.{i.replace('.py', '')}"

            try:
                bot.load_extension(cmdname)
                bot.logger.info(f"{cmdname} Cog successfully loaded.")

            except Exception as error:
                bot.logger.error(f"{cmdname} failed to load: {error}")


bot = Dukzl()
