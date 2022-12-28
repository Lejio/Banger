import random
from discord.ext import commands

class rand(commands.Cog):

  def __init__(self, bot):

    self.bot = bot

  @commands.command("rolldice")
  async def roll_dice(self, ctx, sides):

    await ctx.send("The result is: " + str(random.randint(1, int(sides))))


  @roll_dice.error
  async def roll_dice_error(self, ctx, error):

    await ctx.send("I can't roll anything other than a number!")


  @commands.command("flipcoin")
  async def coin_flip(self, ctx):

    flip = int(random.randint(0, 1))
    if flip == 1:

      await ctx.send("The result is: HEADS")

    else:

      await ctx.send("The result is: TAILS")


async def setup(bot):

  await bot.add_cog(rand(bot))
