import abc
import enum
import string
import typing

import discord

from . import types
from .utils import calculate_remaining_places, get_playstyle_roles_from_member, get_runners_roles_from_member,  runner_role_names, playstyle_role_names
from redbot.core.utils.chat_formatting import humanize_list

if typing.TYPE_CHECKING:
    from redbot.core import commands


class Roles(enum.Enum):
    CYBERACME = 1367066118266556416
    NUCALORIC = 1367066155591925810
    TRAXUS = 1367066328057249833
    SEKIGUCHI = 1367066427542077530
    MIDA = 1367066480407216240


class Colors(enum.Enum):
    MARATHON = discord.Color.from_str("#c4ff0e")
    CYBERACME = discord.Color.from_str("#6dca09")
    NUCALORIC = discord.Color.from_str("#cc0d58")
    TRAXUS = discord.Color.from_str("#e06822")
    SEKIGUCHI = discord.Color.from_str("#93f4c3")
    MIDA = discord.Color.from_str("#8edfe9")


class RequestEmbedBuilder(abc.ABC):
    @staticmethod
    def get_substitutes(ctx: "RequestContext") -> dict[str, str]:
        return {
            "user_name": ctx.author.mention,
            "request_players": str(ctx.looking_for),
            "voice_channel": ctx.voice_channel.mention,
            "remaining_room": str(calculate_remaining_places(ctx.voice_channel)),
            "currently_connected": str(len(ctx.voice_channel.members)),
        }

    @abc.abstractmethod
    def build(
        self,
        ctx: "RequestContext",
    ) -> discord.Embed:
        raise NotImplementedError()


class DefaultEmbedBuilder(RequestEmbedBuilder):
    DEFAULT_MESSAGE = string.Template(
        (
            "Runner **$user_name** is looking to play with **$request_players** other "
            "player(s)!"
        )
    )

    def build(self, ctx: "RequestContext"):
        embed = discord.Embed(
            title=(
                f"LFG request: {ctx.remaining_places} runners left"
                if ctx.remaining_places > 1
                else f"LFG request: {ctx.remaining_places} runner left"
            )
        )
        embed.description = self.DEFAULT_MESSAGE.safe_substitute(self.get_substitutes(ctx))
        
        # Currently connected members
        embed.add_field(
            name="Current runners",
            value="\n".join(member.mention for member in ctx.voice_channel.members) or "No one???",
        )
        embed.add_field(
            name="Channel",
            value=ctx.voice_channel.mention,            
        )
        embed.add_field(name="\u200B", value="\u200B")
        embed.add_field(
            name="Runner",
            value=humanize_list(runner_role_names(get_runners_roles_from_member(ctx.author))),
            inline=True
        )
        # embed.add_field(
        #     name="Language",
        #     value="To set"
        # )
        embed.add_field(
            name="Focus",
            value=humanize_list(playstyle_role_names(get_playstyle_roles_from_member(ctx.author))),
            inline=True
        )

        embed.color = Colors.MARATHON.value
        
        return embed


class CyberAcmeEmbedBuilder(RequestEmbedBuilder):
    def build(self, ctx: "RequestContext"):
        DEFAULT_MESSAGE = string.Template(
            (
                "User **$user_name** is looking to play with **$request_players** other "
                "player(s)!\n"
                "Currently connected to $voice_channel ($currently_connected/$remaining_room)"
            )
        )
        embed = discord.Embed(
            title=(
                f"LFG request: {ctx.looking_for} runners"
                if ctx.looking_for > 1
                else f"LFG request: {ctx.looking_for} runner"
            )
        )
        embed.description = DEFAULT_MESSAGE.safe_substitute(
            {
                "user_name": ctx.author.mention,
                "request_players": str(ctx.looking_for),
                "voice_channel": ctx.voice_channel.mention,
                "remaining_room": calculate_remaining_places(ctx.voice_channel),
                "currently_connected": len(ctx.voice_channel.members),
            }
        )
        embed.add_field(
            name="Runner",
            value=humanize_list(runner_role_names(get_runners_roles_from_member(ctx.author)))
        )
        # embed.add_field(
        #     name="Language",
        #     value="To set"
        # )
        embed.add_field(
            name="Focus",
            value=humanize_list(playstyle_role_names(get_playstyle_roles_from_member(ctx.author)))
        )
        embed.color = ctx.author.color
        return embed


class NuCaloricEmbedBuilder(RequestEmbedBuilder):
    def build(self, ctx: "RequestContext"):
        return discord.Embed(title="NuCaloric")


class TraxusEmbedBuilder(RequestEmbedBuilder):
    def build(self, ctx: "RequestContext"):
        return discord.Embed(title="Traxus")


class SekiguchiGeneticsEmbedBuilder(RequestEmbedBuilder):
    def build(self, ctx: "RequestContext"):
        return discord.Embed(title="Sekiguchi Genetics")


class MIDAEmbedBuilder(RequestEmbedBuilder):
    def build(self, ctx: "RequestContext"):
        return discord.Embed(title="MIDA")


class EmbedBuilderFactory:
    builders: dict[str, type[RequestEmbedBuilder]] = {
        "default": DefaultEmbedBuilder,
        "cyberacme": CyberAcmeEmbedBuilder,
        "nucaloric": NuCaloricEmbedBuilder,
        "traxus": TraxusEmbedBuilder,
        "sekiguchi_genetics": SekiguchiGeneticsEmbedBuilder,
        "MIDA": MIDAEmbedBuilder,
    }

    def selected_builder_string(self, roles: "list[discord.Role]"):
        """Get the string key of the selected builder based on the user's roles.

        Parameters
        ----------
        roles : list[discord.Role]
            The member's roles list.
        """
        match [r.id for r in roles]:
            case [Roles.CYBERACME.value, *_]:
                return "cyberacme"
            case [Roles.NUCALORIC.value, *_]:
                return "nucaloric"
            case [Roles.TRAXUS.value, *_]:
                return "traxus"
            case [Roles.SEKIGUCHI.value, *_]:
                return "sekiguchi_genetics"
            case [Roles.MIDA.value, *_]:
                return "MIDA"
            case _:
                return "default"

    def get_builder_class(
        self, roles: "list[discord.Role]"
    ) -> type[RequestEmbedBuilder]:
        """Returns a non-instantiated builder class based on the user's roles.

        Parameters
        ----------
        user : discord.Member
            The member's roles list.

        Returns
        -------
        type[RequestEmbedBuilder]
            The builder class to instantiate.
        """
        str_version = self.selected_builder_string(roles)
        return self.builders[str_version]

    def get_builder(self, ctx: "RequestContext") -> RequestEmbedBuilder:
        """Returns the instanciated builder.

        Parameters
        ----------
        ctx : RequestContext
            The request context.

        Returns
        -------
        RequestEmbedBuilder
            The embed builder.
        """
        builder_class = self.get_builder_class(ctx.author.roles)
        return builder_class()


class RequestContext:
    author: discord.Member
    """The author of the request."""

    voice_channel: discord.VoiceChannel
    """The voice channel the author is associated to."""

    looking_for: int
    """The number of players the author is looking for."""

    notification: discord.Message | None
    """The notification message sent to the LFG channel."""

    embed_builder: RequestEmbedBuilder
    """The embed builder to use for this request."""

    def __init__(
        self,
        author: "discord.Member",
        voice_channel: "discord.guild.VocalGuildChannel",
        looking_for: int,
    ) -> None:
        self.author = author
        self.voice_channel = author.voice.channel  # type: ignore
        self.looking_for = looking_for
        self.notification = None
        self.embed_builder = EmbedBuilderFactory().get_builder(self)

    @property
    def remaining_places(self) -> int:
        return self.looking_for - len(self.voice_channel.members) + 1

class Request:

    def __init__(
        self,
        author: discord.Member,
        voice_channel: "discord.guild.VocalGuildChannel",
        looking_for: int,
    ):
        self.ctx = RequestContext(author, voice_channel, looking_for)

    def make_embed(self):
        return self.ctx.embed_builder.build(self.ctx)

class RequestCollection:
    current_requests: dict[int, dict[int, Request]]
    """Contains the list of current LFG requests by guild_id and user_id."""
    current_lfgs: dict[types.GuildID, dict[types.UserID, Request]]

    def __init__(self):
        self.current_lfgs = {}

    def push_request(
        self, guild_id: types.GuildID, user_id: types.UserID, request: Request
    ) -> None:
        guild_requests = self.current_lfgs.get(guild_id)
        if guild_requests is None:
            guild_requests = {}
            self.current_lfgs[guild_id] = guild_requests
        guild_requests[user_id] = request

    def has_request(self, guild_id: types.GuildID, user_id: types.UserID) -> bool:
        guild_requests = self.current_lfgs.get(guild_id)
        return guild_requests is not None and guild_requests.get(user_id) is not None

    def get_request(
        self, guild_id: types.GuildID, user_id: types.UserID
    ) -> typing.Optional[Request]:
        guild_requests = self.current_lfgs.get(guild_id)
        if guild_requests is None:
            return None
        return guild_requests.get(user_id)

    def get_request_by_voice_channel_id(
        self, guild_id: types.GuildID, voice_channel_id: int
    ) -> typing.Optional[Request]:
        """Get a request by its voice channel ID.
        
        Parameters
        ----------
        guild_id : types.GuildID
            The ID of the guild where the request is located.
        voice_channel : int
            The ID of the voice channel where the request is located.
        
        Returns
        -------
        typing.Optional[Request]
            The request object if found, otherwise None.
        """
        guild_requests = self.current_lfgs.get(guild_id)
        if guild_requests is None:
            return None
        for request in guild_requests.values():
            if request.ctx.voice_channel.id == voice_channel_id:
                return request
        return None

    def pop_request(
        self, guild_id: types.GuildID, user_id: types.UserID
    ) -> typing.Optional[Request]:
        guild_requests = self.current_lfgs.get(guild_id)
        if guild_requests is None:
            return None
        return guild_requests.pop(user_id, None)
