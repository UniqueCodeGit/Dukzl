import discord
from discord.ext import commands
from wrapper.instagram import Instagram
from config import COLOR

class Chatting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "안녕", aliases=["하이"])
    async def hello (self, ctx):
        embed = discord.Embed (
            title = "👋 왔다네 왔다네 내가 왔다네!",
            description = "이하이 봇은 여러분의 하이 덕질을 도와드리는 봇 입니다! (하이는 소듕하니까요..)\n자세한 명령어들은 `하이야 도움`을 통해 확인해보세요!",
            color = COLOR
        )
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/785166283209048096/791688756792655872/hello.png")
        await ctx.send (embed=embed)

    @commands.command(name = "테스트")
    async def test (self, ctx, code):
        embed = discord.Embed (
            title = "인스타그램 테스트"
        )
        url = await Instagram.DownloadOneImage(code)
        embed.set_image(url = url)
        await ctx.send(embed=embed)
        

def setup (bot):
    bot.add_cog(Chatting(bot))