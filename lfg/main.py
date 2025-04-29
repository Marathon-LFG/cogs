import typing
from click import Choice
from redbot.core import commands
from redbot.core import app_commands
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

    @commands.hybrid_command(name="lfg")
    @app_commands.choices(players=[
        app_commands.Choice(name="1 player", value=1),
        app_commands.Choice(name="2 players", value=2)
    ])
    @app_commands.describe(players="The number of players you are looking for to make a group. Must be contained between \"1\" and \"2\".")
    @app_commands.guilds(1279299830442627074)
    @app_commands.guild_only()
    async def lfg(self, ctx: "commands.GuildContext", players: int):
        """Create a new LFG post for group-making."""
        if not ctx.author.voice:
            await ctx.send("You're not in a voice channel.", ephemeral=True)
        
        await ctx.send(f"LFG, you're looking for {players} players.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: "discord.Member", before: "discord.VoiceState", after: "discord.VoiceState"):
        if has_joined_voice_channel(before, after):
            pass
        if has_left_voice_channel(before, after):
            pass
