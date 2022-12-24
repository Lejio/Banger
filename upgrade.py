import os
from discord.ext import commands

if __name__ == "__name__":

  print("Running upgrade.")
  
  TOKEN = os.getenv('TOKEN')
  
  bot = commands.Bot(command_prefix='!')
  
  @bot.event
  async def on_ready():
  
    print(f"{bot.user.name} has connected to discord!")
  
  bot.run(TOKEN)