import typing


if typing.TYPE_CHECKING:
    import discord


def has_joined_voice_channel(
    state_before: "discord.VoiceState", state_after: "discord.VoiceState"
) -> bool:
    return (state_before.channel is None) and (state_after.channel is not None)


def has_left_voice_channel(
    state_before: "discord.VoiceState", state_after: "discord.VoiceState"
) -> bool:
    return (state_before.channel is not None) and (state_after.channel is None)
