import typing

from redbot.core.commands import check

if typing.TYPE_CHECKING:
    import discord
    from redbot.core.commands import Context, GuildContext

    from lfg.objects import RequestCollection


def is_in_voice_channel():

    async def predicate(ctx: Context) -> bool:
        if isinstance(ctx.author, "discord.Member"):
            return ctx.author.voice is not None
        return False

    return check(predicate)


async def check_can_start_request(
    ctx: "GuildContext", players: int, requests: "RequestCollection"
) -> bool:
    if requests.has_request(ctx.guild.id, ctx.author.id):
        await ctx.send(
            "You already have an active LFG request. Complete it before creating a new one.",
            ephemeral=True,
        )
        return False

    if players < 1 or players > 2:
        await ctx.send("The number of players must be between 1 and 2.", ephemeral=True)
        return False
    if not ctx.author.voice:
        await ctx.send("You're not in a voice channel.", ephemeral=True)
        return False
    if not ctx.author.voice.channel:
        await ctx.send(
            "You're not in a voice channel, or I am not able to find your voice channel. If you are connected to a voice channel, please contact an administrator about this issue.",
            ephemeral=True,
        )
        return False
    # if ctx.author.voice.channel.category_id != 1364881154334789632:
    #     await ctx.send(
    #         "You're not connected to a LFG voice channel. Please connect to <#1364881155559784539> and retry.",
    #         ephemeral=True,
    #     )
    #     return False
    return True
