import discord
import random
import datetime
from discord.ext import commands
from wrapper.userjson import DukzlUsers
from wrapper.artistjson import DukzlArtist
from config import COLOR

class DukzlCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Users = DukzlUsers()
        self.Artists = DukzlArtist()
        self.ElementList = ['생일', '인스타그램', '멜론', '유튜브', '본명', '프로필사진', '프사', '대표곡', '사클', '키', '몸무게', '소속사', '생년월일', '인스타', '유튭', '사운드클라우드', '회사']

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

    @commands.command(name = "탈덕")
    async def removeartist (self, ctx, artist):
        if not self.Users.CheckRegistered(ctx.author):
            return await ctx.send ("가입이 안된 유저입니다. `$가입`을 통해 덕질봇에 가입하시고 모든 서비스를 누려보세요!")
        if not self.Users.CheckArtistExists(ctx.author, artist):
            return await ctx.send ("해당 가수는 덕질하지 않습니다. 가수를 올바르게 입력했는지 확인해주세요.")
        await ctx.send ("정말로 탈덕하시겠습니까? 탈덕하시려면 `탈덕` 을 입력하주세요.")
        response = await self.bot.wait_for (
            "message", 
            check=lambda message: message.author == ctx.author,
            timeout = 60
        )
        if response.content == "탈덕":
            self.Users.RemoveArtist(ctx.author, artist)
            await ctx.send ("성공적으로 탈덕하였습니다.")
        else: await ctx.send ("탈덕을 취소하였습니다.")

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
        if not self.Users.CheckArtistExists(ctx.author, artist):
            return await ctx.send ("해당 가수는 덕질하지 않습니다. 가수를 올바르게 입력했는지 확인해주세요.")
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
                value = f"{artistData['level']}exp - {round(float(artistData['level'])/5, 1)} 레벨", inline=False
            )
            embed.add_field (
                name = "플레이리스트",
                value = f"{len(artistData['playlist'])} 곡 들어있음", inline=False
            )
            await ctx.send (embed=embed)
        except KeyError:
            await ctx.send ("해당 가수는 덕질하지 않습니다. 가수를 올바르게 입력했는지 확인해주세요.")

    @commands.command(name = "플레이리스트추가", aliases=["플리추가"])
    async def addpl (self, ctx, artist, *, url):
        if not self.Users.CheckRegistered(ctx.author):
            return await ctx.send ("가입이 안된 유저입니다. `$가입`을 통해 덕질봇에 가입하시고 모든 서비스를 누려보세요!")
        if not self.Users.CheckArtistExists(ctx.author, artist):
            return await ctx.send ("해당 가수는 덕질하지 않습니다. 가수를 올바르게 입력했는지 확인해주세요.")
        try:
            self.Users.LevelUp(ctx.author,round(random.uniform(2,4),1),artist)
            self.Users.AddPlaylist(ctx.author, artist, url)
            await ctx.send ("성공적으로 플레이리스트에 해당 노래를 넣었습니다.")
        except KeyError:
            await ctx.send ("해당 가수는 덕질하지 않습니다. 가수를 올바르게 입력했는지 확인해주세요.")

    @commands.command(name = "플레이리스트삭제", aliases=["플리삭제"])
    async def poppl (self, ctx, artist, *, url):
        if not self.Users.CheckRegistered(ctx.author):
            return await ctx.send ("가입이 안된 유저입니다. `$가입`을 통해 덕질봇에 가입하시고 모든 서비스를 누려보세요!")
        if not self.Users.CheckArtistExists(ctx.author, artist):
            return await ctx.send ("해당 가수는 덕질하지 않습니다.  가수를 올바르게 입력했는지, URL이 올바른지 확인해주세요.")
        try:
            self.Users.LevelUp(ctx.author,round(random.uniform(1,2),1),artist)
            self.Users.RemovePlaylist(ctx.author, artist, url)
            await ctx.send ("성공적으로 플레이리스트에 해당 노래를 삭제했습니다.")
        except KeyError:
            await ctx.send ("해당 가수는 덕질하지 않습니다. 가수를 올바르게 입력했는지, URL이 올바른지 확인해주세요.")

    @commands.command(name = "플레이리스트리샛", aliases=["플리리셋"])
    async def resetpl (self, ctx, artist):
        if not self.Users.CheckRegistered(ctx.author):
            return await ctx.send ("가입이 안된 유저입니다. `$가입`을 통해 덕질봇에 가입하시고 모든 서비스를 누려보세요!")
        if not self.Users.CheckArtistExists(ctx.author, artist):
            return await ctx.send ("해당 가수는 덕질하지 않습니다. 가수를 올바르게 입력했는지 확인해주세요.")
        try:
            await ctx.send ("정말로 리셋하시겠습니까? 리셋하시려면 `리셋` 을 입력하주세요.")
            response = await self.bot.wait_for (
                "message", 
                check=lambda message: message.author == ctx.author,
                timeout = 60
            )
            if response.content == "리셋":
                self.Users.LevelUp(ctx.author,round(random.uniform(0,1),1),artist)
                self.Users.ResetPlaylist(ctx.author, artist)
                await ctx.send ("성공적으로 플레이리스트를 리셋하였습니다.")
            else: await ctx.send ("리셋을 취소하였습니다.")
        except KeyError:
            await ctx.send ("해당 가수는 덕질하지 않습니다. 가수를 올바르게 입력했는지 확인해주세요.")

    @commands.command(name = "플레이리스트보기", aliases=["플리보기"])
    async def viewpl (self, ctx, artist):
        if not self.Users.CheckRegistered(ctx.author):
            return await ctx.send ("가입이 안된 유저입니다. `$가입`을 통해 덕질봇에 가입하시고 모든 서비스를 누려보세요!")
        if not self.Users.CheckArtistExists(ctx.author, artist):
            return await ctx.send ("해당 가수는 덕질하지 않습니다. 가수를 올바르게 입력했는지 확인해주세요.")
        try:
            data = self.Users.ReturnPlaylist(ctx.author, artist)
            embed = discord.Embed (
                title = f"**{artist}** - 나의 플레이리스트입니다.",
                description = "\n".join(data[:]),
                color = COLOR
            )
            await ctx.send(embed=embed)
        except KeyError:
            await ctx.send ("해당 가수는 덕질하지 않습니다. 가수를 올바르게 입력했는지 확인해주세요.")

    @commands.command(name = "가수정보")
    async def artistinfo (self, ctx, artist):
        if not self.Users.CheckRegistered(ctx.author):
            return await ctx.send ("가입이 안된 유저입니다. `$가입`을 통해 덕질봇에 가입하시고 모든 서비스를 누려보세요!")
        try:
            data = self.Artists.ReturnJson(artist)
            if self.Users.CheckArtistExists(ctx.author, artist):
                self.Users.LevelUp(ctx.author,round(random.uniform(0,1),1),artist)
            embed = discord.Embed(
                title = f"{artist}의 정보입니다.", color = COLOR
            )
            d = (lambda x: "(없음)" if x == "" else x)(data['name'])
            embed.add_field(
                name = "예명",
                value = f"{d}"
            )
            d = (lambda x: "(없음)" if x == "" else x)(data['real_name'])
            embed.add_field(
                name = "본명",
                value = f"{d}"
            )
            d = (lambda x: "(없음)" if x == "" else x)(data['birthday'])
            
            embed.add_field(
                name = "생일",
                value = f"{d}"
            )
            d = (lambda x: "(없음)" if x == "" else x)(f"{data['instagram']}")
            d = (lambda x: "(없음)" if x == "(없음)" else f"[클릭]({x})")(d)
            embed.add_field(
                name = "인스타그램",
                value = f"{d}"
            )
            d = (lambda x: "(없음)" if x == "" else x)(f"{data['melon']}")
            d = (lambda x: "(없음)" if x == "(없음)" else f"[클릭]({x})")(d)
            embed.add_field(
                name = "멜론",
                value = f"{d}"
            )
            d = (lambda x: "(없음)" if x == "" else x)(f"{data['youtube']}")
            d = (lambda x: "(없음)" if x == "(없음)" else f"[클릭]({x})")(d)
            embed.add_field(
                name = "유튜브",
                value = f"{d}"
            )
            embed.set_image(url=data['profilepic'])
            await ctx.send(embed=embed)
        except FileNotFoundError: await ctx.send("해당 가수가 덕질봇 데이터베이스에 없습니다.")

    @commands.command(name="정보추가")
    async def addinfo (self, ctx, *args):
        if not self.Users.CheckRegistered(ctx.author):
            return await ctx.send ("가입이 안된 유저입니다. `$가입`을 통해 덕질봇에 가입하시고 모든 서비스를 누려보세요!")
        try:
            artist = args[0]
            element = args[1]
            obj = args[2]
            if not self.Users.CheckArtistExists(ctx.author, artist):
                return await ctx.send ("해당 가수는 덕질하지 않습니다. 가수를 올바르게 입력했는지 확인해주세요. (띄어쓰기가 없어야 합니다.)")
            self.Users.LevelUp(ctx.author,round(random.uniform(3,5),1),artist)
            if not element in self.ElementList:
                embed = discord.Embed (
                    title = "앗!",
                    description = "정보는 `생일`, `본명`, `인스타그램`, `유튜브`, `멜론`, `프사(프로필사진)` 중 하나여야 합니다.",
                    color = COLOR
                )
                return await ctx.send(embed=embed)
            if element == "생일":
                try:
                    obj = datetime.datetime.strptime(obj, "%Y-%m-%d")
                    obj = obj.strftime("%Y년 %m월 %d일")
                    self.Artists.EditElement(artist, "birthday", obj)
                except ValueError:
                    return await ctx.send ("생일은 YYYY-MM-DD (예시 : 2020-01-01) 형식으로 입력해주세요.")
            if element == "본명" or element == "이름":
                self.Artists.EditElement(artist, "real_name", obj)
            elif element == "인스타그램" or element == "인스타" :
                self.Artists.EditElement(artist, "instagram", obj)
            elif element == "유튜브":
                self.Artists.EditElement(artist, "youtube", obj)
            elif element == "멜론":
                self.Artists.EditElement(artist, "melon", obj)
            elif element == "프사" or element == "프로필사진":
                self.Artists.EditElement(artist, "profilepic", obj)
            await ctx.send ("성공적으로 가수 정보를 수정하였습니다.")
        except FileNotFoundError: await ctx.send("해당 가수가 덕질봇 데이터베이스에 없습니다.")
        except IndexError:
            embed = discord.Embed (
                title = "에러 발생!",
                description = "$정보추가 `가수` `수정할 항목` `내용`으로 제대로 압력했는지 확인해주세요.",
                color = COLOR
            )
            await ctx.send (embed=embed)


def setup (bot):
    bot.add_cog(DukzlCog(bot))