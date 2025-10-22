import typing

from .main import LFG

if typing.TYPE_CHECKING:
    from redbot.core.bot import Red


async def setup(bot: "Red"):
    cog = LFG(bot)
    await bot.add_cog(cog)
