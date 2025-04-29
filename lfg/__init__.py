import typing
from .main import LFG

if typing.TYPE_CHECKING:
    from redbot.core.bot import Red


async def setup(bot: "Red"):
    await bot.add_cog(LFG(bot))
