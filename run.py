import discord
import aiomysql
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
            intents=discord.Intents.all()
        )
        load_extensions(self)
        self.logger = Logger.basicLogger(self)
        self.discordLogger = Logger.discordLogger()
        self.loop = asyncio.get_event_loop()
        self.Wonstein = discodo.DPYClient(self)


    async def create_dbpool(self):
        self.db = await aiomysql.create_pool (
            host=config.DB_IP,
            user=config.DB_USER,
            password=config.DB_PW,
            db="leehi",
            autocommit=True,
            loop=self.loop,
            charset="utf8mb4"
        )


    async def on_message(self, message):
        if not message.author.bot:
            return await self.process_commands(message)

    async def on_ready(self):
        self.logger.info(f"Dukzl loaded as {self.user.name}")

    async def on_command_error(self, context, exception):

        if isinstance(exception, commands.CommandInvokeError):
            embed = discord.Embed(
                title=f"{context.command.name} 수행 중 에러 발생!",
                description="UniqueCode 서포트 서버로 와서 에러 내용을 제보해주세요!",
                color=config.COLOR
            )
            embed.add_field(
                name="에러 내용",
                value=f"```{exception}```"
            )
            await context.send(embed=embed)


bot = Dukzl()
bot.run(config.TOKEN, bot=True)
