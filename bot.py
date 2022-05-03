import os
import discord
import json
from discord.ext import commands
import requests
import asyncio

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    # load a new clip in case one isn't there already
    try:
        clip = get_audio_owen_wilson_clip()
        download_audio_file(clip)
    except:
        print("Something went wrong getting an owen wilson clip")


def get_audio_owen_wilson_clip():
    random_clip = requests.get(
        "https://owen-wilson-wow-api.herokuapp.com/wows/random")
    if random_clip.status_code != 200:
        print("Something went wrong")
    else:
        response_body = json.loads(random_clip.text)
        return response_body[0]['audio']


def download_audio_file(url):
    try:
        r = requests.get(url)
        with open("wilson.mp3", 'wb') as f:
            f.write(r.content)
    except:
        print("Something went wrong downloading the audio file")


@bot.command(
    name='wow',
    description='Wow',
    pass_context=True,
)
async def wow(context):

    # grab the user who sent the command
    user = context.message.author
    voice_channel = user.voice.channel

    # only play music if user is in a voice channel
    if voice_channel != None:

        # create StreamPlayer
        try:
            vc = await voice_channel.connect()  
        except:
            print("Could not connect to voice")
            return

        # wait some time after connecting to the channel to play the clip
        await asyncio.sleep(1)

        vc.play(discord.FFmpegPCMAudio('wilson.mp3'),
                after=lambda e: print('done', e))
        await context.send('Wow!')

        # spin while audio is playing
        while vc.is_playing():
            await asyncio.sleep(1)

        # disconnect after the player has finished
        await asyncio.sleep(1)
        await vc.disconnect()
    else:
        await context.send('User is not in a channel.')

    # refresh clip
    try:
        clip = get_audio_owen_wilson_clip()
        download_audio_file(clip)
    except:
        print("Something went wrong getting an owen wilson clip")


bot.run(TOKEN)
