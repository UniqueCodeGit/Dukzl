import asyncio
import os
from typing import Any

from discord.ext import commands

from config import OWNERS


async def start_discodo() -> Any:
    cmd = "python3 -m discodo --port 6974 --auth SEXSEXSEX"
    return await asyncio.create_subprocess_shell(cmd)


def load_extensions(bot: commands.Bot) -> None:
    cmdlist = os.listdir("cogs/")
    for i in cmdlist:
        if i.endswith(".py") and not i.startswith("__"):
            cmdname = f"cogs.{i.replace('.py', '')}"
            bot.load_extension(cmdname)
    bot.load_extension("jishaku")


async def is_owner(ctx: commands.Context) -> bool:
    if not ctx.author.id in OWNERS:
        await ctx.send("> 봇 오너만 가능한 명령어입니다!")
        return False
    return True


async def check_voice(ctx: commands.Context) -> bool:
    if not ctx.bot.Wonstein.getVC(ctx.guild.id, safe=True):
        if not ctx.author.voice:
            await ctx.send("> 먼저 음성 채널에 접속해주세요!")
            return False
        await ctx.bot.Wonstein.connect(ctx.author.voice.channel)
        await ctx.send(f"> {ctx.author.voice.channel.mention} 에 접속하였습니다!")
    Audio = ctx.bot.Wonstein.getVC(ctx.guild.id, safe=True)
    if Audio and not hasattr(Audio, "channel"):
        Audio.channel = ctx.channel
    return True
