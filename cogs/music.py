import discord
from discord.ext import commands
from . import check_voice
from utils.embed import Embed
from log import Log


class MainCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.logger = Log.cogLogger(self)

    @commands.command(name="join")
    async def join(self, ctx):
        if not ctx.message.author.voice:
            embed = Embed.warn(title="먼저 음성 채널에 들어와주세요!")
            return await ctx.send(embed=embed)
        await self.bot.Wonstein.connect(ctx.message.author.voice.channel)
        embed = Embed.default(
            title=f"성공적으로 {ctx.message.author.voice.channel}에 연결했습니다."
        )
        await ctx.send(embed=embed)

    @commands.command(name="play")
    @commands.check(check_voice)
    async def play(self, ctx, *, query: str):
        Audio = self.bot.Wonstein.getVC(ctx.guild.id)
        await Audio.setAutoplay(False)
        if not Audio:
            embed = Embed.warn(title="먼저 `!join`을 입력해주세요.")
            return await ctx.send(embed=embed)
        Data = await Audio.loadSource(query)
        if isinstance(Data, list):
            Data = Data[0]
        Source, Index = Data["data"], Data["index"] + 1
        self.logger.info(Source)
        if Index == 1:
            await ctx.send(f'> 🎵  {Source["title"]}이 곧 재생되어요!')
        else:
            await ctx.send(f'> 🎵  {Source["title"]}이 대기열 **{Index}**번에 추가되었어요!')


def setup(bot):
    bot.add_cog(MainCog(bot))
