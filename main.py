import asyncio

import discord
from decouple import config
from discord import Message

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
    sussy_words = ['sus', 'cac', 'сус', 'сассать']

    guild = message.guild
    print(message.content, sussy_words)
    if any(ext in message.content for ext in sussy_words):
        await message.channel.send("❗❗❗❗ SUSSY ALERT ❗❗❗❗")

        v_channel = await guild.create_voice_channel(f"Sussy jail ")
        await message.author.move_to(v_channel)

        vc = await v_channel.connect(self_mute=True, timeout=5)

        player = vc.create_ffmpeg_player('sus.mp3', after=lambda: print('done'))

        player.start()
        while not player.is_done():
            await asyncio.sleep(1)
        # disconnect after the player has finished
        player.stop()
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
