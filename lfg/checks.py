import typing
from redbot.core.commands import check, Context

if typing.TYPE_CHECKING:
    import discord

def is_in_voice_channel():

    async def predicate(ctx: Context) -> bool:
        if isinstance(ctx.author, "discord.Member"):
            return ctx.author.voice is not None
        return False

    return check(predicate)
