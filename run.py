import discord
from discord.ext import commands
from config import TOKEN, COLOR
from utils.general import GenerelUtils
from log import Logger

class Dukzl(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=["$"],
            help_command=None,
            activity = discord.Game("$도움 | Dukzl 1.0"),
            intents=discord.Intents.all()
        )
        GenerelUtils.AutoCommands(self)
        self.logger = Logger.basicLogger(self)
        self.discordLogger = Logger.discordLogger()

    async def on_message(self, message):
        if not message.author.bot:
            return await self.process_commands(message)

    async def on_ready(self):
        self.logger.info(f"Dukzl loaded as {self.user.name}")

    async def on_command_error(self, context, exception):
        
        if isinstance (exception, commands.CommandInvokeError):
            embed = discord.Embed(
                title = f"{context.command.name} 수행 중 에러 발생!",
                description = "UniqueCode 서포트 서버로 와서 에러 내용을 제보해주세요!",
                color = COLOR
            )
            embed.add_field (
                name = "에러 내용",
                value = f"```{exception}```"
            )
            await context.send (embed=embed)



bot = Dukzl()
bot.run (TOKEN, bot=True)