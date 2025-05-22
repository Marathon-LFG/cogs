import abc
from calendar import c
import enum
import string
import typing
import discord

from lfg.utils import calculate_remaining_places

if typing.TYPE_CHECKING:
    from redbot.core import commands


class Roles(enum.Enum):
    CYBERACME = 1367066118266556416
    NUCALORIC = 1367066155591925810
    TRAXUS = 1367066328057249833
    SEKIGUCHI = 1367066427542077530
    MIDA = 1367066480407216240


class RequestEmbedBuilder(abc.ABC):
    DEFAULT_MESSAGE = string.Template(
        (
            "User **$user_name** is looking to play with **$request_players** other "
            "player(s)!\n"
            "Currently connected to $voice_channel ($currently_connected/$remaining_room)"
        )
    )
    
    @staticmethod
    def get_substitutes_dict(request: "Request", user: "discord.Member", voice_channel: "discord.VoiceChannel") -> dict[str, str]:
        return {
            "user_name": user.mention,
            "voice_channel": voice_channel.mention,
            "looking_for": str(request.looking_for),
            "remaining_room": str(calculate_remaining_places(voice_channel)),
            "currently_connected": str(len(voice_channel.members))
        }

    @abc.abstractmethod
    def build(self, ctx: "commands.GuildContext") -> discord.Embed:
        raise NotImplementedError()

class CyberAcmeEmbedBuilder(RequestEmbedBuilder):
    def build(self, ctx: "commands.GuildContext"):
        embed = discord.Embed(
            title=(
                f"LFG request: {self.looking_for} runners" if self.looking_for > 1 else f"LFG: {self.looking_for} player"
            )
        )
        embed.description = self.DEFAULT_MESSAGE.safe_substitute({
            "user_name": ctx.author.mention,
            "voice_channel": ctx.author.voice.channel.mention,
            "remaining_room": calculate_remaining_places(ctx.author.voice.channel),
            "currently_connected": len(ctx.author.voice.channel.members)
        })
        embed.color = ctx.author.color
        return embed


class NuCaloricEmbedBuilder(RequestEmbedBuilder):
    def build(self, ctx: "commands.GuildContext"):
        return discord.Embed()


class TraxusEmbedBuilder(RequestEmbedBuilder):
    def build(self, ctx: "commands.GuildContext"):
        return discord.Embed()


class SekiguchiGeneticsEmbedBuilder(RequestEmbedBuilder):
    def build(self, ctx: "commands.GuildContext"):
        return discord.Embed()


class MIDAEmbedBuilder(RequestEmbedBuilder):
    def build(self, ctx: "commands.GuildContext"):
        return discord.Embed()


class EmbedBuilderFactory:
    builders: dict[str, type[RequestEmbedBuilder]] = {
        "default": RequestEmbedBuilder,
        "cyberacme": CyberAcmeEmbedBuilder,
        "nucaloric": NuCaloricEmbedBuilder,
        "traxus": TraxusEmbedBuilder,
        "sekiguchi_genetics": SekiguchiGeneticsEmbedBuilder,
        "MIDA": MIDAEmbedBuilder
    }
    
    def get_builder(self, user: "discord.Member") -> type[RequestEmbedBuilder]:
        pass


class Request:
    author: discord.Member
    
    looking_for: int

    def __init__(self, author: discord.Member, looking_for: int):
        self.author = author
        self.looking_for = looking_for

    # def obtain_embed(self, remaining_room: int):
    #     return

class RequestCollection:
    current_requests: dict[int, dict[int, Request]]
    """Contains the list of current LFG requests by guild_id and user_id."""

    def __init__(self):
        self.current_lfgs = {}

    def has_request(self, user_id: int, guild_id: int) -> bool:
        guild_requests = self.current_lfgs.get(guild_id)
        return guild_requests is not None and guild_requests.get(user_id) is not None
