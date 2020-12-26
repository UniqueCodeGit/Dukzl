import discord
import psutil
import cpuinfo
import platform
from discord.ext import commands
from config import COLOR
from EZPaginator import Paginator

class Chatting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "안녕", aliases=["하이", "ㅎㅇ"])
    async def hello (self, ctx):
        embed = discord.Embed (
            title = "👋 왔다네 왔다네 내가 왔다네!",
            description = "덕질봇은 여러분들의 가수 덕질을 도와드리는 봇 입니다!\n자세한 명령어들은 `$도움`을 통해 확인해보세요!",
            color = COLOR
        )
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/785166283209048096/791688756792655872/hello.png")
        await ctx.send (embed=embed)

    @commands.command(name = "help", aliases = ["도움", "명령어들", "명렁어"])
    async def helpcmd(self, ctx):
        embed = discord.Embed(
            title = "Dukzl 봇 도움말 입니다.",
            description = "페이지를 넘기면서 세부사항을 확인하세요!",
            color = COLOR
        )
        embed.add_field (
            name = "1페이지",
            value = "Dukzl - 유저", inline=False
        )
        embed.add_field (
            name = "2페이지",
            value = "Dukzl - 가수", inline=False
        )
        embed.add_field (
            name = "3페이지",
            value = "음악", inline=False
        )
        embed.add_field (
            name = "4페이지",
            value = "일반", inline=False
        )
        embed1 = discord.Embed (
            title = "1페이지",
            description = "유저 관련 명령어입니다.", color = COLOR
        )
        embed1.add_field(
            name = "`$가입`", value = "덕질봇 서비스에 가입합니다.", inline=False
        )
        embed1.add_field(
            name = "`$가수추가 (가수이름)`", value = "나의 덕질 목록에 가수를 한명 추가합니다.", inline=False
        )
        embed1.add_field(
            name = "`$탈덕 (가수이름)`", value = "해당 가수를 탈덕합니다.", inline=False
        )
        embed1.add_field(
            name = "`$내정보`", value = "나의 서비스 이용 상태를 확인할 수 있습니다.", inline=False
        )
        embed1.add_field(
            name = "`$덕질정보 (가수이름)`", value = "해당 가수에 대한 내 덕질 현황을 볼 수 있습니다.", inline=False
        )
        embed1.add_field(
            name = "`$플리추가 (가수이름) (유튜브 URL 혹은 키워드)`", value = "해당 유튜브 링크를 덕질 플레이리스트에 추가합니다.", inline=False
        )
        embed1.add_field(
            name = "`$플리삭제 (가수이름) (유튜브 URL 혹은 키워드)`", value = "해당 유튜브 링크를 덕질 플레이리스트에서 삭제합니다.", inline=False
        )
        embed1.add_field(
            name = "`$플리리셋 (가수이름)`", value = "해당 가수의 덕질 플레이리스트를 리셋합니다.", inline=False
        )
        embed1.add_field(
            name = "`$플리재생 (가수이름)`", value = "해당 가수의 덕질 플레이리스트를 재생합니다.", inline=False
        )
        embed2 = discord.Embed (
            title = "2페이지",
            description = "가수 관련 명령어 입니다.", color = COLOR
        )
        embed2.add_field(
            name = "`$가수정보 (가수이름)`", value = "해당 가수의 정보를 조회합니다.", inline=False
        )
        embed2.add_field(
            name = "`$정보추가 (가수이름) (요소) (내용)`", value = "해당 가수의 정보를 추가합니다. 요소는 생일, 본명, 인스타그램, 유튜브, 멜론, 프사 중 하나여야 합니다.", inline=False
        ) 
        embed3 = discord.Embed (
            title = "3페이지",
            description = "음악 관련 명렁어 입니다.", color = COLOR
        )
        embed3.add_field (
            name = "`$p (키워드)`", value = "해당 음악을 재생합니다.", inline=False
        )
        embed3.add_field (
            name = "`$skip`", value = "현재 음악을 스킵합니다.", inline=False
        )
        embed3.add_field (
            name = "`$stop`", value = "음악을 멈춥니다.", inline=False
        )
        embed3.add_field (
            name = "`$np`", value = "현재 음악을 보여줍니다.", inline=False
        )
        embed3.add_field (
            name = "`$pause`", value = "음악을 일시정시 / 재개합니다.", inline=False
        )
        embed3.add_field (
            name = "`$repeat`", value = "음악을 반복합니다. (토글형식)", inline=False
        )
        embed3.add_field (
            name = "`$shuffle`", value = "음악을 셔플합니다. (토글형식)", inline=False
        )
        embed3.add_field (
            name = "`$volume (1~100)`", value = "볼륨을 설정합니다. 그냥 명령어만 입력하면 현재 볼륨을 출력합니다.", inline=False
        )
        embed3.add_field (
            name = "`$queue`", value = "현재 재생목록을 보여줍니다.", inline=False
        )
        embed3.add_field (
            name = "`$remove (인덱스)`", value = "해당 음악을 재생목록에서 지웁니다.", inline=False
        )
        embed3.add_field (
            name = "`$leave`", value = "통화방에서 나갑니다.", inline=False
        )
        embed4 = discord.Embed (
            title = "4페이지",
            description = "일반 관련 명령어 입니다.", color = COLOR
        )
        embed4.add_field(
            name = "`$안녕`", value = "봇이 인사를 합니다.", inline=False
        )
        embed4.add_field(
            name = "`$핑`", value = "현재 핑을 출력합니다.", inline=False
        )
        embed4.add_field(
            name = "`$정보`", value = "봇의 정보를 출력합니다.", inline=False
        )
        embed4.add_field(
            name = "`$도움`", value = "이 명령어 입니다.", inline=False
        )
        embeds = [embed, embed1, embed2, embed3, embed4]
        msg = await ctx.send(embed=embed)
        page = Paginator(self.bot, msg, embeds=embeds)
        await page.start()


    @commands.command(name = "ping", aliases = ["핑"])
    async def pingg(self, ctx):
        t1 = ctx.message.created_at
        ctx2 = await ctx.send('메시지 핑 테스트용 입니다. 무시해주셔도 좋습니다!')
        t2 = ctx2.created_at
        ping = t2 - t1
        pp = str(int(ping.microseconds) / 1000)
        pp = pp.split(".")
        pp = pp[0]
        embed = discord.Embed(title="Pong!", color = COLOR)
        embed.add_field(
            name="Websocket", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="메시지 핑", value=f"{pp}ms", inline=True)
        await ctx2.edit(embed=embed, content="")

    @commands.command(name = "정보", aliases = ["서버정보", "server"])
    async def about(self, ctx): 
        ramstatus = psutil.virtual_memory()
        ramm = str(
            f"{round((ramstatus[0]/1000000000)-(ramstatus[1]/1000000000), 2)}GB / {round(ramstatus[0]/1000000000, 2)}GB")
        ramm = str(ramm.replace("['", ""))
        ramm = str(ramm.replace("']'", ""))
        cpu = cpuinfo.get_cpu_info()
        embed = discord.Embed(title="Dukzl 정보", color = COLOR)
        embed.add_field(name="봇 버전", value="0.1 HACKATHON", inline=False)
        embed.add_field(name="CPU", value=cpu['brand_raw'], inline=False)
        embed.add_field(name="RAM Usage", value=ramm, inline=False)
        embed.add_field(name="Architecture", value=cpu["arch"], inline=False)
        embed.add_field(name="OS", value=platform.platform(), inline=False)
        embed.add_field(name="API 핑", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        await ctx.send(embed=embed)


        

def setup (bot):
    bot.add_cog(Chatting(bot))