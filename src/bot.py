import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.command(name='ping', help='Responds with Hello')
async def ping(ctx):
    await ctx.send('pong')