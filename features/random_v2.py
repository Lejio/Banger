import random
from discord.ext import commands
from discord import app_commands
from datetime import datetime
import discord

class rand(commands.Cog):

  def __init__(self, bot):

    self.bot = bot

  @app_commands.command(name="rolldice", description="Returns a number within the given range. If none given, the default would be 6.")
  async def roll_dice(self, interaction: discord.Interaction, sides: int=None):
    if sides == None:

      sides = 6

    embed = discord.Embed(title="Dice Roll", description=f"The result of a {sides} sided dice is **{str(random.randint(1, int(sides)))}**.", color=discord.Colour.yellow(), timestamp=datetime.utcnow())
    
    await interaction.response.send_message(embed=embed)



  @app_commands.command(name="flipcoin", description="Flips a coin. Returns heads or tails.")
  async def coin_flip(self, interaction: discord.Interaction):

    flip = int(random.randint(0, 1))
    if flip == 1:

      result = "HEADS"

    else:

      result = "TAILS"

    embed = discord.Embed(title="Coin Flip", description=f"The result is **{result}**", color=discord.Colour.yellow(), timestamp=datetime.utcnow())
    await interaction.response.send_message(embed=embed)
    

async def setup(bot):

  await bot.add_cog(rand(bot))
