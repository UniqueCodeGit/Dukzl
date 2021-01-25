import discord
import asyncio
import orjson
import os
import streamlink
from discord.ext import commands
from wrapper.twitch import TwitchAPI
from utils.embed import Embed
from . import is_owner


class Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Twitch = TwitchAPI()

    @commands.command(name="토큰테스트")
    @commands.check(is_owner)
    async def tokentest(self, ctx, *, scopes=None):
        token = await self.Twitch.get_twitch_token(scopes)
        user = self.bot.get_user(ctx.author.id)
        await user.send(token)
        await ctx.send(f"Twitch API 토큰이 생성되었습니다. DM을 확인해주세요. <@!{ctx.author.id}>")

    @commands.command(name="scope")
    async def scopelist(self, ctx):
        await ctx.send("https://dev.twitch.tv/docs/authentication#scopes")

    @commands.command(name="유저테스트")
    @commands.check(is_owner)
    async def test_helix_user(self, ctx, id):
        data = await self.Twitch.get_users(id)
        await ctx.send(f"```{data}```")

    @commands.command(name="ID테스트")
    @commands.check(is_owner)
    async def getID_test(self, ctx, id):
        data = await self.Twitch.getID(id)
        await ctx.send(data)

    @commands.command(name="방송테스트")
    @commands.check(is_owner)
    async def stream_test(self, ctx, id):
        data = await self.Twitch.get_streams(id)
        data = orjson.loads(data)
        await ctx.send(f'```{data["data"]}```')

    @commands.command(name="게임테스트")
    @commands.check(is_owner)
    async def game_test(self, ctx, *i):
        id = " ".join(i[:])
        data = await self.Twitch.get_game(id)
        data = orjson.loads(data)
        await ctx.send(f"```{data}```")

    @commands.command(name="체크테스트")
    @commands.check(is_owner)
    async def check_stream_test(self, ctx, id):
        data = await self.Twitch.check_streaming(id)
        await ctx.send(data)

    @commands.command(name="유저정보")
    async def user_info(self, ctx, id):
        data = await self.Twitch.get_users(id)
        data = orjson.loads(data)
        check = await self.Twitch.check_streaming(id)
        try:
            embed = Embed(title=f'{data["data"][0]["display_name"]} ({id}) 정보')
            embed.add_field(
                name="방송 중",
                value=(lambda v: "방송중 입니다." if v == True else "방송 중이 아닙니다.")(check),
                inline=True,
            )
            await ctx.send(embed=embed)
        except (KeyError, IndexError):
            await ctx.send("ID가 바르지 않습니다. 다시 한번 ID를 확인해주세요.")

    @commands.command(name="방송정보")
    async def stream_info(self, ctx, id):
        try:
            game = None
            data = await self.Twitch.get_streams(id)
            data = orjson.loads(data)
            if data["data"][0]["game_id"]:
                game = await self.Twitch.getGame(data["data"][0]["game_id"])
                game = orjson.loads(game)
                game = game["data"][0]
            data = data["data"][0]
            embed = Embed(title=f'{data["title"]} - {data["user_name"]}')
            await ctx.send(embed=embed)
        except (KeyError, IndexError):
            await ctx.send("ID가 바르지 않습니다. 다시 한번 ID를 확인해주세요.")

    @commands.command(name="게임정보")
    async def game_info(self, ctx, *id):
        try:
            id = " ".join(id[:])
            data = await self.Twitch.get_game(id)
            data = orjson.loads(data)
            data = data["data"][0]
            embed = discord.Embed(title="게임 정보")
            embed.add_field(name="API 고유 ID", value=f'{data["id"]}')
            embed.add_field(name="게임 이름", value=f'{data["name"]}')
            uri = data["box_art_url"]
            uri = uri.replace("{width}", "512")
            uri = uri.replace("{height}", "512")
            embed.set_thumbnail(url=uri)
            await ctx.send(embed=embed)
        except (KeyError, IndexError):
            await ctx.send("게임 이름을 확인해주세요.")

    @commands.command(name="방송움짤")
    async def gif(self, ctx, name):
        check = await self.Twitch.check_streaming(name)
        if check:
            turl = f"https://www.twitch.tv/{name}"
            streams = streamlink.streams(turl)
            stream = streams["160p"].url
            ffset = ["ffmpeg", "-i", stream, "-t", "00:00:03", f"{name}.gif"]
            p = await asyncio.create_subprocess_shell(
                " ".join(ffset),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await p.communicate()
            embed = Embed(title=name).set_image(url=f"attachment://{name}.gif")
            await ctx.send(file=discord.File(f"{name}.gif"), embed=embed)
            try:
                os.remove(f"{name}.gif")
            except Exception:
                pass
        else:
            await ctx.send("해당 스트리머가 방송중이지 않습니다.")


def setup(bot: commands.Bot):
    bot.add_cog(Twitch(bot))
