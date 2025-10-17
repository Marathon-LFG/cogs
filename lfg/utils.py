import logging
import typing

if typing.TYPE_CHECKING:
    import discord


log = logging.getLogger("red.marathon.lfg")

RUNNER_ROLES = (
    1365736777704276118,  # Locus
    1365736778467901550,  # Glitch (my beloved)
    1365736779134664704,  # Blackbird
    1365736780078252257,  # My second beloved
)

PLAYSTYLE_ROLES_IDS = (
    1365736951323557980,  # PvP
    1365736953676300388,  # PvE
)


def get_runners_roles_from_member(member: "discord.Member") -> list["discord.Role"]:
    """Return the list of runner roles only.
    This is mostly used when building an embed, and to allow to see which runners are played by a
    member.

    Parameters
    ----------
    member : discord.Member
        The member to check.

    Returns
    -------
    list[discord.Role]
        The runner roles.
    """
    return [role for role in member.roles if role.id in RUNNER_ROLES]


def runner_role_names(roles: "list[discord.Role]") -> list[str]:
    """Return the list of runner roles names without the cool-looking prefix.

    Parameters
    ----------
    roles : list[discord.Role]
        The runner roles.

    Returns
    -------
    list[str]
        The runner role names.
    """
    return [role.name.strip("RUNNER://") for role in roles]


def get_playstyle_roles_from_member(member: "discord.Member") -> list["discord.Role"]:
    """Return the list of playstyle roles only.

    Parameters
    ----------
    member : discord.Member
        The member to check.

    Returns
    -------
    list[discord.Role]
        The playstyle roles.
    """
    return [role for role in member.roles if role.id in PLAYSTYLE_ROLES_IDS]


def playstyle_role_names(roles: "list[discord.Role]") -> list[str]:
    """Return the list of playstyle roles names without the cool-looking prefix.

    Parameters
    ----------
    roles : list[discord.Role]
        The runner roles.

    Returns
    -------
    list[str]
        The runner role names.
    """
    return [role.name.strip("FOCUS://") for role in roles]


def has_joined_voice_channel(
    state_before: "discord.VoiceState", state_after: "discord.VoiceState"
) -> bool:
    """Check if a member has joined a voice channel.

    Parameters
    ----------
    state_before : discord.VoiceState
        Before state.
    state_after : discord.VoiceState
        After state.

    Returns
    -------
    bool
        If the member has joined a voice channel.
    """
    return (state_before.channel is None) and (state_after.channel is not None)


def has_left_voice_channel(
    state_before: "discord.VoiceState", state_after: "discord.VoiceState"
) -> bool:
    """Check between state if a member has left a voice channel.

    Parameters
    ----------
    state_before : discord.VoiceState
        Before state.
    state_after : discord.VoiceState
        After state.

    Returns
    -------
    bool
        If the member has left a voice channel.
    """
    return (state_before.channel is not None) and (state_after.channel is None)


def calculate_remaining_places(
    channel: "discord.channel.VocalGuildChannel",
) -> int | None:
    """Calculates the remaining places availables in a voice channel.

    Parameters
    ----------
    channel : discord.channel.VocalGuildChannel
        The voice channel to calculate.

    Returns
    -------
    int | None
        The total remaining places, or None if there is no limit.
    """
    if channel.user_limit == 0:
        return None
    return channel.user_limit - len(channel.members)
