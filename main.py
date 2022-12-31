import asyncio
import io
import json
import shutil
from asyncio import sleep

import discord
import requests
from PIL import Image
from decouple import config
from discord import Message, Member, VoiceState, VoiceChannel, File
from discord.ext import commands
from discord.ext.commands import Context
from gtts import gTTS
from io import StringIO

TOKEN = config("BOT_TOKEN")
TPN_TOKEN = config("TPN_TOKEN")
FFMPEG_PATH = config("FFMPEG_PATH")

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(intents=intents, command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Welcome to the rice fields, {member.name},!")


async def play_audio(v_channel, file: str | bytes):
    vc = await v_channel.connect(self_mute=False, self_deaf=True, timeout=5)

    audio = discord.FFmpegPCMAudio(file, executable=FFMPEG_PATH, pipe=file is bytes)
    vc.play(audio)

    while vc.is_playing():
        await sleep(0.1)

    await vc.disconnect()


@bot.event
async def on_message(message: Message):
    sussy_words = ["sus", "сас", "сус", "сассать"]

    if any(ext in message.content for ext in sussy_words):
        await message.channel.send("❗❗❗❗ SUSSY ALERT ❗❗❗❗")

        if message.author.voice.channel is None:
            return

        await play_audio(message.author.voice.channel, "sounds/sus.mp3")

    elif message.content == "raise-exception":
        raise discord.DiscordException

    await bot.process_commands(message)


@bot.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    if member.name == "MishaBot":
        return

    if after.channel is not None and not after.mute and before.channel is None:
        myobj = gTTS(
            text=f"Импостер {member.display_name} залетел в {after.channel.name}!",
            lang="ru",
            slow=True,
        )
        myobj.save("kekw.mp3")
        await play_audio(after.channel, "kekw.mp3")
        await play_audio(after.channel, "sounds/join.mp3")
    elif not before.self_deaf and after.self_deaf:
        myobj = gTTS(
            text=f"{member.display_name} нихуя не слышит!", lang="ru", slow=True
        )
        myobj.save("kekw.mp3")
        await play_audio(after.channel, "kekw.mp3")
    elif before.self_deaf and not after.self_deaf:
        myobj = gTTS(
            text=f"{member.display_name}; пока тебя не было, твою мать выебали!",
            lang="ru",
            slow=True,
        )
        myobj.save("kekw.mp3")
        await play_audio(after.channel, "kekw.mp3")

    elif not before.self_mute and after.self_mute:
        myobj = gTTS(
            text=f"{member.display_name} - хули ты замютился, дибил ебаный?",
            lang="ru",
            slow=True,
        )
        myobj.save("kekw.mp3")
        await play_audio(after.channel, "kekw.mp3")
    elif before.self_mute and not after.self_mute:
        myobj = gTTS(
            text=f"{member.display_name} - бичара вернулся!", lang="ru", slow=True
        )
        myobj.save("kekw.mp3")
        await play_audio(after.channel, "kekw.mp3")


@bot.event
async def on_presence_update(before: Member, after: Member):
    pass


@bot.event
async def on_member_update(before: Member, after: Member):
    if before.roles != after.roles:
        new_roles = []
        old_roles = []
        for role in after.roles:
            if role not in before.roles:
                new_roles.append(role.name)
        for role in before.roles:
            if role not in after.roles:
                old_roles.append(role.name)

        if len(new_roles) > 0:
            myobj = gTTS(
                text=f"Поздравляем {after.display_name} - c получением звания {', '.join(new_roles)}",
                lang="ru",
                slow=True,
            )
            myobj.save("kekw.mp3")
            await play_audio(after.voice.channel, "kekw.mp3")
        else:
            myobj = gTTS(
                text=f"{after.display_name} - ты больше не {', '.join(old_roles)}",
                lang="ru",
                slow=True,
            )
            myobj.save("kekw.mp3")
            await play_audio(after.voice.channel, "kekw.mp3")


@bot.command(name="trace", help="Track CSGO")
async def csgo_track(ctx: Context, nickname):
    response = requests.get(
        url=f"https://public-api.tracker.gg/v2/csgo/standard/profile/steam/{nickname}",
        headers={
            "TRN-Api-Key": f"{TPN_TOKEN}",
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
        },
    )
    if response.status_code != 200:
        await ctx.send("No such user exists?? or smth")
        return

    data = json.loads(response.content.decode("utf-8"))

    juice = data["data"]["segments"][0]["stats"]
    username = data["data"]["platformInfo"]["platformUserHandle"]
    image_url = data["data"]["platformInfo"]["avatarUrl"]

    text = (
        f"Nickname: {username}\n\n"
        f"Time Played: {juice['timePlayed']['displayValue']}\n"
        f"K/D: {juice['kd']['displayValue']}\n"
        f"Accuracy: {juice['shotsAccuracy']['displayValue']}\n"
        f"Headshots: {juice['headshotPct']['displayValue']}\n"
        f"Win Rate: {juice['wlPercentage']['displayValue']}\n"
    )

    pic_response = requests.get(image_url)

    if pic_response.status_code != 200:
        await ctx.send(text)
    else:
        response = requests.get(image_url, stream=True)
        with open("img.png", "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)

        del response
        await ctx.send(text, file=File("img.png", filename="kekw.png"))
    await play_audio(ctx.author.voice.channel, "sounds/gamer.mp3")


if __name__ == "__main__":
    bot.run(TOKEN)
