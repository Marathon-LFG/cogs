import typing


if typing.TYPE_CHECKING:
    import discord


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


def calculate_remaining_places(channel: "discord.VoiceChannel") -> int | None:
    """Calculates the remaining places availables in a voice channel.

    Parameters
    ----------
    channel : discord.VoiceChannel
        The voice channel to calculate.

    Returns
    -------
    int | None
        The total remaining places, or None if there is no limit.
    """
    if channel.user_limit == 0:
        return None
    return channel.user_limit - len(channel.members)
