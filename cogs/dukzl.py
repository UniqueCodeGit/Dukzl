import discord
from discord.ext import commands
from wrapper.userjson import DukzlUsers
from wrapper.artistjson import DukzlArtist
from config import COLOR

class DukzlCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Users = DukzlUsers()
        self.Artists = DukzlArtist()

    @commands.command(name = "가입")
    async def register (self, ctx):
        if self.Users.CheckRegistered(ctx.author):
            return await ctx.send ("이미 가입된 유저입니다.")
        self.Users.RegisterUser(ctx.author)
        embed = discord.Embed (
            title = "축하합니다!",
            description = "가입에 성공하였습니다. 이제 덕질봇 서비스를 이용하세요!",
            color = COLOR
        )
        await ctx.send (embed=embed)

    @commands.command(name = "가수추가")
    async def addartist (self, ctx, artist):
        if not self.Users.CheckRegistered(ctx.author):
            return await ctx.send ("가입이 안된 유저입니다. `$가입`을 통해 덕질봇에 가입하시고 모든 서비스를 누려보세요!")
        if self.Users.CheckArtistExists(ctx.author, artist):
            return await ctx.send ("해당 가수는 이미 덕질중 입니다.")
        self.Users.AddArtist(ctx.author, artist)
        await ctx.send (f"성공적으로 `{artist}`를 덕질 목록에 추가했습니다!")
        if not self.Users.CheckArtistJson(artist):
            await ctx.send (f"해당 아티스트는 덕질봇 데이터베이스에 존재하지 않습니다. 직접 정보를 추가해보세요!")
            self.Artists.MakeArtistJson(artist)
        

    @commands.command(name = "내정보")
    async def myinfo (self, ctx):
        if not self.Users.CheckRegistered(ctx.author):
            return await ctx.send ("가입이 안된 유저입니다. `$가입`을 통해 덕질봇에 가입하시고 모든 서비스를 누려보세요!")
        data = self.Users.ReturnJson(ctx.author)
        embed = discord.Embed (title = "내 덕질 정보 입니다.", color = COLOR)
        embed.add_field (
            name = "이름",
            value = ctx.author.name, inline=False
        )
        embed.add_field (
            name = "서비스 가입 일자",
            value = data["started-date"], inline=False
        )
        embed.add_field (
            name = "덕질하는 가수 수",
            value = f"{len(data['artists'])}명", inline=False
        )
        if len(data['artists']) != 0:
            art = ", ".join(data['artistlist'][:])
            embed.add_field (
                name = "덕질하는 가수",
                value = f"{art}", inline=False
            )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send (embed=embed)

    @commands.command(name = "덕질가수정보", aliases=['덕질정보'])
    async def artistdukzl (self, ctx, artist):
        if not self.Users.CheckRegistered(ctx.author):
            return await ctx.send ("가입이 안된 유저입니다. `$가입`을 통해 덕질봇에 가입하시고 모든 서비스를 누려보세요!")
        try:
            data = self.Users.ReturnJson(ctx.author)
            artistData = {}
            for artists in data["artists"]:
                if artists["name"] == artist:
                    artistData = artists
                    break
            embed = discord.Embed (
                title = f"가수 **{artist}**의 덕질 정보 입니다.", color = COLOR
            )
            embed.add_field (
                name = "덕질을 시작한 날",
                value = artistData["started-date"], inline=False
            )
            embed.add_field (
                name = "덕질 레벨",
                value = f"{artistData['level']} 레벨", inline=False
            )
            embed.add_field (
                name = "플레이리스트",
                value = f"{len(artistData['playlist'])} 곡 들어있음", inline=False
            )
            await ctx.send (embed=embed)
        except KeyError:
            await ctx.send ("해당 가수는 덕질하지 않습니다.")

        



def setup (bot):
    bot.add_cog(DukzlCog(bot))