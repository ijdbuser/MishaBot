import asyncio
from asyncio import sleep

import discord
from decouple import config
from discord import Message, ClientException

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



@client.event
async def on_message(message: Message):
    sussy_words = ['sus', 'сас', 'сус', 'сассать']

    if any(ext in message.content for ext in sussy_words):
        await message.channel.send("❗❗❗❗ SUSSY ALERT ❗❗❗❗")

        if message.author.voice.channel is None:
            return

        v_channel = message.author.voice.channel

        vc = await v_channel.connect(self_mute=False, self_deaf=True, timeout=5)

        audio = discord.FFmpegPCMAudio("sus.mp3", executable="C:\\ffmpeg\\bin\\ffmpeg.exe")
        vc.play(audio)

        while vc.is_playing():
            await sleep(.1)

        await vc.disconnect()

    elif message.content == 'raise-exception':
        raise discord.DiscordException

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise




if __name__ == "__main__":
    client.run(TOKEN)
