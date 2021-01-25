import discord
import datetime
import config
from dateutil import tz


class EmbedUtil:
    def __init__(self):
        pass

    @classmethod
    def datetime_to_kr(cls, timestamp) -> str:
        from_zone = tz.tzutc()
        to_zone = tz.gettz("Asia/Seoul")
        d = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        d = d.replace(tzinfo=from_zone)
        d = d.astimezone(tz=to_zone)
        d = d.strftime("%Y년 %m월 %d일 %H시 %M분")
        return d

    @classmethod
    def author(cls, embed=discord.Embed, author=discord.abc.User) -> None:
        embed.set_author(name=author, icon_url=author.avatar_url)

    @classmethod
    def footer(cls, embed=discord.Embed) -> None:
        embed.timestamp = datetime.datetime.utcnow()
        embed.color = config.COLOR
        embed.set_footer(text="Dukzl")

    @classmethod
    def twitch_user_embed(cls, data, embed=discord.Embed) -> None:
        embed.add_field(
            name="설명",
            value=(lambda n: "(없음)" if n == "" else n)(data["data"][0]["description"]),
            inline=False,
        )
        embed.add_field(
            name="스트리머 타입",
            value=(lambda broad_type: "파트너" if broad_type == "partner" else "일반")(
                data["data"][0]["broadcaster_type"]
            ),
            inline=True,
        )
        embed.add_field(
            name="API 고유 ID",
            value=(lambda n: "(없음)" if n == "" else n)(data["data"][0]["id"]),
            inline=True,
        )
        embed.add_field(
            name="총 조회수",
            value=(lambda n: "(없음)" if n == "" else n)(data["data"][0]["view_count"]),
            inline=True,
        )
        if data["data"][0]["profile_image_url"]:
            embed.set_thumbnail(url=data["data"][0]["profile_image_url"])
        if data["data"][0]["offline_image_url"]:
            embed.set_image(url=data["data"][0]["offline_image_url"])

    @classmethod
    def twitch_stream_embed(cls, data, embed: discord.Embed, game) -> None:
        embed.add_field(
            name="API 고유 유저 ID",
            value=(lambda n: "(없음)" if n == "" else n)(data["user_id"]),
            inline=True,
        )
        embed.add_field(
            name="API 고유 방송 ID",
            value=(lambda n: "(없음)" if n == "" else n)(data["id"]),
            inline=True,
        )
        if game:
            embed.add_field(
                name="게임 이름",
                value=(lambda n: "(없음)" if n == "" else n)(game["name"]),
                inline=True,
            )
        if data["started_at"]:
            dd = cls.getDateTime(data["started_at"])
            embed.add_field(
                name="시작 시각",
                value=(lambda n: "(없음)" if n == "" else n)(dd),
                inline=True,
            )
        embed.add_field(
            name="현재 시청자 수",
            value=(lambda n: "(없음)" if n == "" else f"{n}명")(data["viewer_count"]),
            inline=True,
        )
        uri = data["thumbnail_url"]
        uri = uri.replace("{width}", "1920")
        uri = uri.replace("{height}", "1080")
        if data["thumbnail_url"] is not None:
            embed.set_image(url=uri)