import discord
import asyncio
import discodo
import config
from discord.ext import commands
from log import Logger
from cogs import load_extensions


class Dukzl(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=["$"],
            help_command=None,
            activity=discord.Game("$도움 | Dukzl 1.0"),
            intents=discord.Intents.all(),
        )
        load_extensions(self)
        self.logger = Logger.cogLogger(self)
        self.discordLogger = Logger.discordLogger()
        self.Wonstein = discodo.DPYClient(self)

    async def on_message(self, message):
        if not message.author.bot:
            return await self.process_commands(message)

    async def on_ready(self):
        self.logger.info(f"Dukzl loaded as {self.user.name}")

    async def on_command_error(self, context, exception):
        if isinstance(exception, commands.CommandInvokeError):
            embed = discord.Embed(
                title=f"{context.command.name} 수행 중 에러 발생",
                description="Dukzl 서버에서 버그 제보를 해주세요!",
                color=config.COLOR,
            )
            embed.add_field(name="에러 내용", value=f"```{exception}```")
            await context.send(embed=embed)


bot = Dukzl()
bot.run(config.TOKEN, bot=True)
