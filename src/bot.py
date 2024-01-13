from .utilities.stream import get_url_audio_source
from collections import deque
import asyncio
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

    while playlist:
        source = playlist.popleft()
        source.read()   # This prevents audio from speeding at the beginning

        vc.play(source)
        while vc.is_paused() or vc.is_playing():
            await asyncio.sleep(1)  # TODO: Figure out how to do this without sleep

    # Done with playlist
    playlists.pop(ctx.guild.id)
    await vc.disconnect()

@bot.event
async def on_command_error(ctx: commands.Context, error: Exception):
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
async def play(ctx: commands.Context, url: str, add_order: str = 'now'):
    print(f'Play request: url={url}, add_order={add_order}')

    # TODO: Resume playing
    if url is None:
        return

    # Invalid add_order
    if add_order not in ['now', 'next', 'last']:
        await ctx.send(f'`"{add_order}" must be one of: "now", "next", "last", or simply omit`')
        return

    # Get stream
    try:
        source = get_url_audio_source(url)
    except Exception as e:
        print(f'Could not get source from url={url}: {e}')
        raise

    # Replace
    vc = ctx.voice_client
    if vc and add_order == 'now':   # If already playing, replace
        print('HERE 1')
        vc.stop()
        print('HERE 2')
        vc.play(source)
        print('HERE 3')
        return

    # Add next/last
    playlist: deque = playlists.get(ctx.guild.id, None)
    if playlist:    # If playlist exists, add song
        if add_order == 'next':
            playlist.appendleft(source)
        else:
            playlist.append(source)

    # Starting worker
    if not ctx.author.voice:    # Author must be in a voice channel when starting player
        await ctx.send('`Please connect to the channel before requesting music to play. Bip bop`')
        return

    playlist = deque([source])
    asyncio.ensure_future(execute_player_worker(ctx, playlist))

@bot.command(help='Bot pauses playing audio')
async def pause(ctx: commands.Context):
    vc = ctx.voice_client
    if not vc:
        return

    vc.pause()
