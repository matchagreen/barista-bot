from typing import Optional
from .utilities.song import Song
from collections import deque
import asyncio
import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

playlists: dict[str, deque[Song]] = {}

def on_song_end(error: Exception, event: asyncio.Event):
    if error: print(f'Finished song with error: {error}')
    event.set()

async def execute_player_worker(ctx: commands.Context, playlist: deque):
    global playlists
    playlists[ctx.guild.id] = playlist

    next_song_event = asyncio.Event()
    vc = await ctx.author.voice.channel.connect()

    while playlist:
        song = playlist.popleft()
        song.source.read()  # This prevents audio from speeding at the beginning

        vc.play(song.source, after=lambda error: on_song_end(error, next_song_event))
        await next_song_event.wait()
        next_song_event.clear()

    # Clean up
    del playlists[ctx.guild.id]
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

@bot.command(help='Resumes or starts an audio player on the channel in which the user is located.')
async def play(ctx: commands.Context, url: Optional[str], add_order: str = 'now'):
    print(f'Play request: url={url}, add_order={add_order}')

    # Resume playing
    vc = ctx.voice_client
    if url is None:
        if not vc:
            return await ctx.send(f'`Cannot resume playing. I am not currently in a voice channel. Bip bop`')

        return vc.resume()

    # Invalid add_order
    if add_order not in ['now', 'next', 'last']:
        await ctx.send(f'`"{add_order}" must be one of: "now", "next", "last", or simply omit. Bip bop`')
        return

    # Get stream
    try:
        song = Song(url)
    except Exception as e:
        print(f'Could not get source from url={url}: {e}')
        raise

    # Replace current song
    if vc and add_order == 'now':
        playlists[ctx.guild.id].appendleft(song)
        return vc.stop()

    # If bot is playing, add next/last
    if ctx.guild.id in playlists:
        playlist = playlists[ctx.guild.id]
        if add_order == 'next':
            playlist.appendleft(song)
        else:
            playlist.append(song)

        titles_list = ''.join([f'- {song.title}\n' for song in playlist])
        return await ctx.send(f'`Current queue:\n{titles_list}`')

    # Starting worker
    if not ctx.author.voice:    # Author must be in a voice channel when starting player
        return await ctx.send('`Please connect to the channel before requesting music to play. Bip bop`')

    playlist = deque([song])
    asyncio.ensure_future(execute_player_worker(ctx, playlist))

@bot.command(help='Pause audio')
async def pause(ctx: commands.Context):
    vc = ctx.voice_client
    if not vc:
        return

    vc.pause()

@bot.command(help='Stop player')
async def stop(ctx: commands.Context):
    vc = ctx.voice_client
    if not vc:
        return

    playlists[ctx.guild.id].clear()
    vc.stop()

@bot.command(help='Skips the current song')
async def skip(ctx: commands.Context):
    vc = ctx.voice_client
    if not vc:
        return

    vc.stop()