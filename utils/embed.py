from __future__ import annotations

from typing import Optional

import discord
from discord.ext.commands.context import Context

from config import COLOR

DEFAULT_COLOR = COLOR
WARN_COLOR = 0xD8EF56
ERROR_COLOR = 0xFF0909


class Embed(discord.Embed):
    """ Embed utility class (Thanks to BGM) """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def default(
            cls,
            title: Optional[str] = None,
            description: Optional[str] = None,
            **kwargs,
    ) -> Embed:
        self = cls.__new__(cls)
        self.__init__(title=f"{title}", description=description, **kwargs)
        return self

    @classmethod
    def warn(
            cls,
            title: Optional[str] = None,
            description: Optional[str] = None,
            **kwargs,
    ) -> Embed:
        self = cls.__new__(cls)
        self.__init__(
            title=f"⚠ {title}",
            description=f"{description}",
            color=WARN_COLOR,
            **kwargs,
        )
        return self

    @classmethod
    def error(
            cls,
            title: Optional[str] = None,
            description: Optional[str] = None,
            **kwargs,
    ) -> Embed:
        self = cls.__new__(cls)
        self.__init__(
            title=f"❌ {title}",
            description=f"{description}",
            color=ERROR_COLOR,
            **kwargs,
        )
        return self

    def user_footer(self, ctx: Context) -> Embed:
        self.set_footer(
            text=f"{ctx.author} | {ctx.bot.user.name}#{ctx.bot.user.discriminator}",
            icon_url=ctx.author.avatar_url,
        )
        return self
