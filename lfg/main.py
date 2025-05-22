import email
import typing
from click import Choice
from redbot.core import commands
from redbot.core import app_commands

from lfg.objects import Request, RequestCollection
# from redbot.core.config import Config

from .utils import has_joined_voice_channel, has_left_voice_channel

if typing.TYPE_CHECKING:
    import discord
    from redbot.core.bot import Red


class LFG(commands.Cog):
    """LFG system for Marathon group-making."""
    
    def __init__(self, bot: "Red"):
        self.bot: "Red" = bot
        
        # self.config: "Config" = Config.get_conf(self, identifier=55856177615, force_registration=True)
        # self.config.register_guild()
        
        self.requests = RequestCollection()

    @commands.hybrid_command(name="lfg")
    @app_commands.choices(players=[
        app_commands.Choice(name="1 player", value=1),
        app_commands.Choice(name="2 players", value=2)
    ])
    @app_commands.describe(players="The number of players you are looking for to make a group.")
    @app_commands.guilds(1279299830442627074, 1364692913438589098)  # Remove after initial development.
    @app_commands.guild_only()
    async def lfg(self, ctx: "commands.GuildContext", players: int):
        """Create a new LFG post for group-making.
        
        __Parameters__
        ``players``: The number of players you are looking for to make a group.
            Must be between 1 and 2.
        """
        if players < 1 or players > 2:
            await ctx.send("The number of players must be between 1 and 2.", ephemeral=True)
            return
        # if not ctx.author.voice:
        #     await ctx.send("You're not in a voice channel.", ephemeral=True)
        #     return
        # if not ctx.author.voice.channel:
        #     await ctx.send("You're not in a voice channel, or I am not able to find your voice channel.", ephemeral=True)
        #     return
        # if ctx.author.voice.channel.category_id != 1364881154334789632:
        #     await ctx.send("You're not connected to a LFG voice channel. Please connect to <#1364881155559784539> and retry.", ephemeral=True)
        #     return

        request = Request(ctx.author, players)
        
        remaining_room = ctx.author.voice.channel.user_limit - len(ctx.author.voice.channel.members)
        e = request.obtain_embed(remaining_room=remaining_room)
        
        await ctx.send(embed=e, ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: "discord.Member", before: "discord.VoiceState", after: "discord.VoiceState"):
        if has_joined_voice_channel(before, after):
            pass
        if has_left_voice_channel(before, after):
            pass
