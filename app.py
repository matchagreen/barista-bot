import os
from src.bot import bot
from src.utilities.dotenv import load_dotenv


load_dotenv()

bot.run(os.environ['BOT_TOKEN'])

