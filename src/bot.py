import asyncio
from pytube import YouTube
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('''`Command format is incorrect. Send "/help {command}" for
 details on how to run a command. Bip bop.
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

    vc = await ctx.author.voice.channel.connect()

    try:
        yt = YouTube(url)

        audio_stream = yt.streams.filter(only_audio=True).first()
        source = discord.FFmpegPCMAudio(audio_stream.url)
        vc.play(source, after=lambda error: print('Player error: ${e}') if error else None)

        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()

    except Exception as e:
        await vc.disconnect()
        raise
