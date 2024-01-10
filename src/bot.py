import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_command_error(ctx, error):
    await ctx.send('''`You forgot to provide a required argument. Send "/help {command}" for
 details on how to run a command.
`''')

@bot.command(help='Plays a youtube link')
async def play(ctx, url):
    print('URL', url)
