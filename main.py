import asyncio
import io
from asyncio import sleep

import discord
from decouple import config
from discord import Message, ClientException, Member, VoiceState, VoiceChannel
from gtts import gTTS

TOKEN = config("BOT_TOKEN")

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Welcome to the rice fields, {member.name},!'
    )


async def play_audio(v_channel, file: str | bytes):
    vc = await v_channel.connect(self_mute=False, self_deaf=True, timeout=5)
    audio = discord.FFmpegPCMAudio(file,
                                   executable="C:\\ffmpeg\\bin\\ffmpeg.exe",
                                   pipe=file is bytes)
    vc.play(audio)

    while vc.is_playing():
        await sleep(.1)

    await vc.disconnect()


@client.event
async def on_message(message: Message):
    sussy_words = ['sus', 'сас', 'сус', 'сассать']

    if any(ext in message.content for ext in sussy_words):
        await message.channel.send("❗❗❗❗ SUSSY ALERT ❗❗❗❗")

        if message.author.voice.channel is None:
            return

        await play_audio(message.author.voice.channel, "sounds/sus.mp3")

    elif message.content == 'raise-exception':
        raise discord.DiscordException


@client.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    if member.name == "MishaBot":
        return

    if after.channel is not None and not after.mute and before.channel is None:
        myobj = gTTS(text=f"Импостер {member.display_name} залетел в {after.channel.name}!", lang='ru', slow=True)
        myobj.save("kekw.mp3")
        await play_audio(after.channel, "kekw.mp3")
        await play_audio(after.channel, "sounds/join.mp3")
    elif not before.self_deaf and after.self_deaf:
        myobj = gTTS(text=f"{member.display_name} нихуя не слышит!", lang='ru', slow=True)
        myobj.save("kekw.mp3")
        await play_audio(after.channel, "kekw.mp3")
    elif before.self_deaf and not after.self_deaf:
        myobj = gTTS(text=f"{member.display_name}; пока тебя не было, твою мать выебали!", lang='ru', slow=True)
        myobj.save("kekw.mp3")
        await play_audio(after.channel, "kekw.mp3")

    elif not before.self_mute and after.self_mute:
        myobj = gTTS(text=f"{member.display_name} - хули ты замютился, дибил ебаный?", lang='ru', slow=True)
        myobj.save("kekw.mp3")
        await play_audio(after.channel, "kekw.mp3")
    elif before.self_mute and not after.self_mute:
        myobj = gTTS(text=f"{member.display_name} - бичара вернулся!", lang='ru', slow=True)
        myobj.save("kekw.mp3")
        await play_audio(after.channel, "kekw.mp3")


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


if __name__ == "__main__":
    client.run(TOKEN)
