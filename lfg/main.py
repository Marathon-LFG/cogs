import typing

import discord
from redbot.core import app_commands, commands

from lfg import checks
from lfg.objects import Request, RequestCollection
from lfg.utils import log

from .utils import (
    calculate_remaining_places,
    has_joined_voice_channel,
    has_left_voice_channel,
)

# from redbot.core.config import Config


if typing.TYPE_CHECKING:
    import discord
    from redbot.core.bot import Red


class LFG(commands.Cog):
    """LFG system for Marathon group-making."""

    requests: RequestCollection

    def __init__(self, bot: "Red"):
        self.bot: "Red" = bot

        # self.config: "Config" = Config.get_conf(self, identifier=55856177615, force_registration=True)
        # self.config.register_guild()

        self.requests = RequestCollection()

        super().__init__()

    @commands.hybrid_command(name="lfg")
    @app_commands.choices(
        players=[
            app_commands.Choice(name="1 player", value=1),
            app_commands.Choice(name="2 players", value=2),
        ]
    )
    @app_commands.describe(
        players="The number of players you are looking for to make a group."
    )
    @app_commands.guilds(
        1279299830442627074, 1364692913438589098
    )  # Remove after initial development.
    @app_commands.guild_only()
    async def lfg(self, ctx: "commands.GuildContext", players: int):
        """Create a new LFG post for group-making.

        __Parameters__
        ``players``: The number of players you are looking for to make a group.
            Must be between 1 and 2.
        """
        if not await checks.check_can_start_request(ctx, players, self.requests):
            return

        assert ctx.author.voice
        assert ctx.author.voice.channel

        request = Request(ctx.author, ctx.author.voice.channel, players)
        self.requests.push_request(ctx.guild.id, ctx.author.id, request)

        e = request.make_embed()

        request_message = await ctx.send(embed=e, ephemeral=True)
        request.ctx.notification = request_message

    @commands.is_owner()
    @commands.command(aliases=["lfginfo"])
    async def lfgkowalskyanalysis(self, ctx: "commands.GuildContext"):
        """Kaboom......??"""
        requests = self.requests.current_lfgs.get(ctx.guild.id)
        if not requests:
            await ctx.send("No active LFG requests.")
            return

        description = "Current requests:\n"
        description += "\n".join(
            f"- {req.ctx.author.mention} | VC: {req.ctx.author.voice.channel if req.ctx.author.voice else None}"
            for req in requests.values()
        )

        embed = discord.Embed(
            title="Current LFG Requests Analysis", description=description
        )
        await ctx.send("Yes Rico... Kaboom!", embed=embed)

    @commands.command(name="lfgdelete")
    @commands.mod_or_can_manage_channel()
    @commands.guild_only()
    async def lfgforcedelete(
        self, ctx: "commands.GuildContext", member: "discord.Member"
    ):
        """Force delete a user's LFG request.

        __Parameters__
        ``member``: The member whose LFG request you want to delete.
        """
        if not self.requests.has_request(ctx.guild.id, member.id):
            await ctx.send(
                f"{member.display_name} has no active LFG request.", ephemeral=True
            )
            return

        self.requests.pop_request(ctx.guild.id, member.id)
        await ctx.send(
            f"{member.display_name}'s LFG request has been deleted.", ephemeral=True
        )

    async def complete_request(self, request: Request):
        if request.ctx.notification:
            await request.ctx.notification.delete()
            await request.ctx.notification.channel.send(
                f"{request.ctx.author.display_name}'s LFG request has been completed and removed.",
                delete_after=10,
            )
        self.requests.pop_request(request.ctx.author.guild.id, request.ctx.author.id)

    async def update_request_embeds(self, request: Request):
        message = request.ctx.notification
        if not message:
            log.error("No notification message found for request. Cannot update embed.")
            return

        remaining_places = calculate_remaining_places(request.ctx.voice_channel)
        if remaining_places is None:
            log.error(
                "Could not calculate remaining places for voice channel. Cannot update embed."
            )
            return
        if remaining_places <= 0:
            await self.complete_request(request)
            return

        embed = request.make_embed()
        await message.edit(embed=embed)

    async def on_voice_leave(
        self, member: "discord.Member", channel: "discord.guild.VocalGuildChannel"
    ):
        request = self.requests.get_request_by_voice_channel_id(
            channel.guild.id, channel.id
        )
        if request:
            await self.update_request_embeds(request)

    async def on_voice_join(
        self, member: "discord.Member", channel: "discord.guild.VocalGuildChannel"
    ):
        request = self.requests.get_request_by_voice_channel_id(
            channel.guild.id, channel.id
        )
        if request:
            await self.update_request_embeds(request)

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: "discord.Member",
        before: "discord.VoiceState",
        after: "discord.VoiceState",
    ):
        log.debug(
            f"Voice state update for {member.display_name}: {before.channel} -> {after.channel}"
        )
        check_against = None
        if before.channel:
            check_against = before.channel
        if after.channel:
            check_against = after.channel
        if not check_against:
            log.error(
                "No before or after channel found for voice status update. Event ignored."
            )
            return

        if has_joined_voice_channel(before, after):
            channel = after.channel
            assert channel
            log.info("Voice channel joined: %s", channel.name)
            await self.on_voice_join(member, channel)

        if has_left_voice_channel(before, after):
            channel = before.channel
            assert channel
            log.info("Voice channel joined: %s", channel.name)
            await self.on_voice_leave(member, channel)
