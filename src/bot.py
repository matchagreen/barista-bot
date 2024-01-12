from collections import deque
import asyncio
from pytube import YouTube
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

playlist = deque()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('''`Command format is incorrect. Send "/help {command}" for
 details on how to run a command. Bip bop
`''')
        return
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('`Command does not exist. Send "/help" for a list of all available commands. Bip bop`')
        return

    await ctx.send('`Something broke 🤖💥 bop bip`')
    raise error

@bot.command(help='Plays the audio from a youtube link')
async def play(ctx, url):
    if not ctx.author.voice:
        await ctx.send('`Please connect to the channel before requesting music to play. Bip bop`')
        return

    # If already playing, replace
    vc = ctx.voice_client
    if vc:
        vc.stop()
        source = get_url_audio_source(url)
        vc.play(source)
        return

    vc = await ctx.author.voice.channel.connect()

    try:
        source = get_url_audio_source(url)
        vc.play(source, after=lambda error: print('Player error: ${e}') if error else None)

        # This will basically run forever as long as the bot keeps playing.
        # One per instance of bot playing
        while True:
            if vc.is_paused() or vc.is_playing():
                await asyncio.sleep(1)
                continue

            if playlist:
                print(f'Playing next song: {url}')
                source = get_url_audio_source(playlist.popleft())
                print(f'Playlist: {[song for song in playlist]}')
                vc.play(source)
                continue

            break

        await vc.disconnect()

    except Exception as e:
        await vc.disconnect()
        raise

@bot.command(help='Adds to queue')
async def play_last(ctx, url):
    print(f'Adding {url} to playlist.')
    playlist.append(url)
    print(f'Playlist: {[song for song in playlist]}')

@bot.command(help='Stops bot from playing audio')
async def stop(ctx):
    vc = ctx.voice_client
    if not vc:
        return

    vc.stop()

@bot.command(help='Bot pauses playing audio')
async def pause(ctx):
    vc = ctx.voice_client
    if not vc:
        return

    vc.pause()

def get_url_audio_source(url: str):
    yt = YouTube(url)

    audio_stream = yt.streams.filter(only_audio=True).first()
    source = discord.FFmpegPCMAudio(audio_stream.url)
    source.read()   # This prevents audio from speeding at the beginning

    return source