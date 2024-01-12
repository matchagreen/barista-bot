from collections import deque
import asyncio
from pytube import YouTube
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

playlists = {}

async def execute_player_worker(ctx: commands.Context, playlist: deque):
    global playlists
    playlists[ctx.guild.id] = playlist
    vc = await ctx.author.voice.channel.connect()

    # Keep running as long as playlist has songs
    while True:
        vc.play(playlist.popleft(), after=lambda e: print(f'Finished playing song.{f" {e}" if e else ""}'))

        while vc.is_paused() or vc.is_playing():
            await asyncio.sleep(1)

        if not playlist:
            break

    playlists.pop(ctx.guild.id)

@bot.event
async def on_command_error(ctx: commands.Context, error):
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
async def play(ctx: commands.Context, url: str):
    if not ctx.author.voice:
        await ctx.send('`Please connect to the channel before requesting music to play. Bip bop`')
        return

    try:
        source = get_url_audio_source(url)
    except Exception as e:
        print(f'Could not get source from url={url}: {e}')
        raise

    # If already playing, replace
    vc = ctx.voice_client
    if vc:
        vc.play(source)
        return

    playlist = deque([source])
    asyncio.ensure_future(execute_player_worker(ctx, playlist))

@bot.command(help='Stops bot from playing audio')
async def stop(ctx: commands.Context):
    vc = ctx.voice_client
    if not vc:
        return

    vc.stop()

@bot.command(help='Bot pauses playing audio')
async def pause(ctx: commands.Context):
    vc = ctx.voice_client
    if not vc:
        return

    vc.pause()

@bot.command(help='')
async def play_next(ctx: commands.Context, url: str):
    playlist: deque = playlists[ctx.guild.id]

    try:
        source = get_url_audio_source(url)
    except Exception as e:
        print(f'Could not get source from url={url}: {e}')
        raise

    playlist.appendleft(source)

@bot.command(help='')
async def play_last(ctx: commands.Context, url: str):
    playlist: deque = playlists[ctx.guild.id]

    try:
        source = get_url_audio_source(url)
    except Exception as e:
        print(f'Could not get source from url={url}: {e}')
        raise

    playlist.append(source)

def get_url_audio_source(url: str):
    yt = YouTube(url)

    audio_stream = yt.streams.filter(only_audio=True).first()
    source = discord.FFmpegPCMAudio(audio_stream.url)
    source.read()   # This prevents audio from speeding at the beginning

    return source