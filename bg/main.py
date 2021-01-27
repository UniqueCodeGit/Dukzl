import asyncio
from log import Log
from wrapper.twitch import TwitchAPI
from discord.ext import commands

async def azi_test(bot: commands.Bot) -> None:
    API = TwitchAPI()
    CH = bot.get_channel(803886723510829097)
    past = API.check_streaming("dkwl025")
    while True:
        asyncio.sleep(60)
        now = API.check_streaming("dkwl025")
        if past != now and now == True:
            await CH.send("양아지방송함 <@!295371171979853825>")