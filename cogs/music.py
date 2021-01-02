import math
import re
import discord
import lavalink
import random
from discord.ext import commands
from wrapper.userjson import DukzlUsers
from config import COLOR

url_rx = re.compile('https?:\\/\\/(?:www\\.)?.+') 
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._ = 791673162046767124
        self.Users = DukzlUsers()
        self.normal_color = COLOR
        if not hasattr(bot, 'lavalink'): 
            bot.lavalink = lavalink.Client(self._)
            bot.lavalink.add_node('localhost', 2333, 'youshallnotpass', 'eu') 
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')
        bot.lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None
        if guild_check:
            await self.ensure_voice(ctx)
        return guild_check

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    async def queue_add(self, ctx, query):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        for i in query:
            i = i.strip('<>')
            #if not url_rx.match(i):
                #i = f'{i}'
            results = await player.node.get_tracks(i)
            if not results or not results['tracks']:
                return await ctx.send(f'재생목록에서 {i}를 넣는데 실패하였습니다.')
            if results['loadType'] == 'PLAYLIST_LOADED':
                tracks = results['tracks']
                for track in tracks:
                    player.add(requester=ctx.author.id, track=track)
            else:
                track = results['tracks'][0]
                player.add(requester=ctx.author.id, track=track)

    @commands.command(name = "플레이리스트재생", aliases=['플리재생'])
    async def play_playlist(self, ctx, artist):
        if not self.Users.CheckRegistered(ctx.author):
            return await ctx.send ("가입이 안된 유저입니다. `$가입`을 통해 덕질봇에 가입하시고 모든 서비스를 누려보세요!")
        if not self.Users.CheckArtistExists(ctx.author, artist):
            return await ctx.send ("해당 가수는 덕질하지 않습니다. 가수를 올바르게 입력했는지 확인해주세요.")
        self.Users.LevelUp(ctx.author, round(random.uniform(4,5),1), artist)
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        data = self.Users.ReturnPlaylist(ctx.author, artist)
        await self.queue_add(ctx, data)
        await ctx.send (f"{artist} 플레이리스트를 재생목록에 추가하였습니다.")
        if not player.is_playing:
            await player.play()

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query: str):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = query.strip('<>')
        #if not url_rx.match(query):
        #    query = f'ytsearch:{query}'
        results = await player.node.get_tracks(query)
        if not results or not results['tracks']:
            return await ctx.send(f'재생목록에서 {query}를 넣는데 실패하였습니다.')
        embed = discord.Embed(color=self.normal_color)
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)
            embed.title = '플레이리스트 로드 완료!'
            embed.description = '성공적으로 플레이리스트를 로드했습니다.'
            embed.add_field (name = "이름", value=f'{results["playlistInfo"]["name"]}', inline=True)
            embed.add_field (name="곡 수", value=str(len(tracks))+"개", inline=True)
            embed.add_field (name = "요청자", value=f"<@!{ctx.author.id}>", inline=True)
        else:
            track = results['tracks'][0]
            embed.title = '트랙 로드 완료!'
            embed.description = f'```{track["info"]["title"]}```'
            embed.add_field (name="URL", value=f'[클릭]({track["info"]["uri"]})', inline=True)
            embed.add_field (name = "요청자", value=f"<@!{ctx.author.id}>", inline=True)
            embed.add_field (name = "길이", value = f'{lavalink.utils.format_time(track["info"]["length"])}', inline=True)
            embed.set_thumbnail(url=f'https://i.ytimg.com/vi/{track["info"]["identifier"]}/hqdefault.jpg')
            player.add(requester=ctx.author.id, track=track)
        await ctx.send(embed=embed)
        if not player.is_playing:
            await player.play()

    @commands.command(aliases=['forceskip'])
    async def skip(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('재생 중 이지 않습니다.')
        await player.skip()
        await ctx.message.add_reaction('\U00002705')

    @commands.command()
    async def stop(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('재생 중 이지 않습니다.')
        player.queue.clear()
        await player.stop()
        await ctx.message.add_reaction('\U00002705')


    @commands.command(aliases=['np', 'n', 'playing'])
    async def now(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.current:
            return await ctx.send('재생 중인 것이 없습니다.')
        position = lavalink.utils.format_time(player.position)
        if player.current.stream:
            duration = 'LIVE'
        else:
            duration = lavalink.utils.format_time(player.current.duration)
        embed = discord.Embed(color=self.normal_color,
                              title='현재 플레이 중',
                              description = f"```{player.current.title}```")
        embed.add_field (
            name = "URL",
            value = f"[클릭]({player.current.uri})"
        )
        embed.add_field (
            name = "위치",
            value = f"{position}/{duration}"
        )
        embed.add_field (
            name = "요청자",
            value = f"<@!{player.current.requester}>"
        )
        embed.set_thumbnail(url=f'https://i.ytimg.com/vi/{player.current.identifier}/hqdefault.jpg')
        await ctx.send(embed=embed)

    @commands.command(aliases=['q'])
    async def queue(self, ctx, page: int = 1):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.queue:
            return await ctx.send('재생목록에 아무것도 없습니다.')
        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)
        start = (page - 1) * items_per_page
        end = start + items_per_page
        queue_list = ''
        for index, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'
        embed = discord.Embed(colour=self.normal_color,
                              description=f'**{len(player.queue)} tracks**\n\n{queue_list}')
        embed.set_footer(text=f'페이지 {page}/{pages}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['resume'])
    async def pause(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('플레이 중이지 않습니다.')
        if player.paused:
            await player.set_pause(False)
        else:
            await player.set_pause(True)
        await ctx.message.add_reaction('\U00002705')

    @commands.command(aliases=['vol'])
    async def volume(self, ctx, volume: int = None):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not volume:
            return await ctx.send(f'현재 볼륨 : {player.volume}%')
        await player.set_volume(volume) 
        await ctx.send(f'볼륨을 {player.volume}% 으로 설정하였습니다.')

    @commands.command()
    async def shuffle(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('재생 중인 것이 없습니다.')
        player.shuffle = not player.shuffle
        await ctx.send('🔀 | 셔플 ' + ('켜짐' if player.shuffle else '꺼짐'))

    @commands.command(aliases=['loop'])
    async def repeat(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('재생 중인 것이 없습니다.')
        player.repeat = not player.repeat
        await ctx.send('🔁 | 반복 ' + ('켜짐' if player.repeat else '꺼짐'))

    @commands.command()
    async def remove(self, ctx, index: int):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.queue:
            return await ctx.send('재생목록에 아무것도 없습니다.')
        if index > len(player.queue) or index < 1:
            return await ctx.send(f'1 과 {len(player.queue)} 사이의 정수를 입력해주세요.')
        removed = player.queue.pop(index - 1)
        await ctx.send(f'**{removed.title}** 가 재생목록에서 제거되었습니다.')

    @commands.command(aliases=['dc', 'leave'])
    async def disconnect(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send('연결되지 않음.')
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('다른 음성 채널에 있어요! 제가 있는 음성 채널로 와주세요.')
        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild.id, None)
        await ctx.message.add_reaction('👋')

    async def ensure_voice(self, ctx):
        player = player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        should_connect = ctx.command.name in ('play')
        should_connect2 = ctx.command.name in ('플레이리스트재생')
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError('먼저 음성 채널에 들어와주세요.')
        if not player.is_connected:
            if should_connect2:
                permissions = ctx.author.voice.channel.permissions_for(ctx.me)
                if not permissions.connect or not permissions.speak:  
                    raise commands.CommandInvokeError('권한이 없습니다! (Connect, Speak 권한을 주세요!)')
                player.store('channel', ctx.channel.id)
                return await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
            if not should_connect:
                raise commands.CommandInvokeError('봇이 연결되지 않았습니다.')
            permissions = ctx.author.voice.channel.permissions_for(ctx.me)
            if not permissions.connect or not permissions.speak:  
                raise commands.CommandInvokeError('권한이 없습니다! (Connect, Speak 권한을 주세요!)')
            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('다른 음성 채널에 있어요! 제가 있는 음성 채널로 와주세요.')


def setup(bot):
    bot.add_cog(Music(bot))