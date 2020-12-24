import discord
from discord.ext import commands
from config import TOKEN, COLOR
from utils.general import GenerelUtils

class Dukzl(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=["$"],
            help_command=None,
            activity = discord.Game("$도움 | 덕질의 세계는 신기해요.."),
            intents=discord.Intents.all()
        )
        GenerelUtils.AutoCommands(self)

    async def on_message(self, message):
        if not message.author.bot:
            return await self.process_commands(message)

    async def on_ready(self):
        print (f"{self.user.name}")

    async def on_command_error(self, context, exception):
        if isinstance (exception, commands.CommandInvokeError):
            embed = discord.Embed(
                title = f"{context.command.name} 수행 중 에러 발생!",
                description = "금방 고칠게요 죄송합니다 ㅠ",
                color = COLOR
            )
            embed.add_field (
                name = "에러 내용",
                value = f"```{exception}```"
            )
            await context.send (embed=embed)



bot = Dukzl()
bot.run (TOKEN, bot=True)