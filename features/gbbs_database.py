from replit import db
from discord.ext import commands


class users(commands.Cog):

  def __init__(self, bot):

    self.bot = bot
    self.BANGERS = 'Bangers'
    self.LVL = 'Lvl'
    self.BADGE = 'Rank'

  def add_user(self, user):

    db[user] = {self.BANGER: 1000, self.LVL: 0, self.BADGE: ":video_game:"}

    return True

  @commands.command("bangers")
  async def get_bangers(self, ctx):
    print(str(ctx.author.id))
    print(str(ctx.author))
    # await db[user][self.BANGER]
    await ctx.send(db[ctx.author][self.BANGERS])

  @get_bangers.error
  async def get_bangers_error(ctx, error):

    print(error)
    await ctx.send("You are not in the database.")

  @commands.command("level")
  async def get_level(self, ctx):

    await ctx.send(db[ctx.author][self.BANGERS])

  def is_guild_owner():

    def predicate(ctx):
      return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id

    return commands.check(predicate)

  @commands.command("check")
  @commands.check_any(commands.is_owner(), is_guild_owner())
  async def retrieve_info(self, ctx, user):

    await ctx.send(db[user])


async def setup(bot):

  await bot.add_cog(users(bot))
