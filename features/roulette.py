import random
from discord.ext import commands
from features.gbbs_database import database
from features.printing import *
import time


class roulette(commands.Cog):

  def __init__(self, bot):

    # self.default_cash = 1000
    self.bot = bot
    # self.players = {}
    self.color = ""
    self.roulette = {
      "GREEN": {},
      "BLACK": {},
      "RED": {}
    }  # Make a function that gets the length of each three colors.
    # self.startgame(self.default_cash)

  # def startgame(
  #   self, default_cash
  # ):

  #   self.default_cash = default_cash

  # @commands.command("jointable")
  # async def addplayer(self, ctx):

  #   if ctx.author in self.players.keys():  # Checks the player's username is a key inside of the dictionary.

  #     await ctx.send("You have already joined the game.")

  #   else:

  #     # If player's name is not inside the dictionary, create a new key.

  #     await ctx.send(f"{player} has joined the game.")

  @commands.command("bet")
  async def betcash(self, ctx, bet_money, color):

    # self.players[ctx.author]["Money"] -= int(bet_money)

    db = database(ctx.guild.id)
    db.change_bangers(-int(bet_money), ctx.author)
    player = db.get_user(ctx.author)

    print(player[3])
    
    if (int(player[3]) < 0):

      db.change_bangers(int(bet_money), ctx.author)

      await ctx.send("`You have insufficient funds.`")

    else:

      if ctx.author in self.roulette[color].keys():

        self.roulette[color][ctx.author] += int(bet_money)

        await ctx.send(f"`{ctx.author} has placed {bet_money} more on {color}`")

      else:

        self.roulette[color][ctx.author] = int(bet_money)

      await ctx.send(f"`{ctx.author} has placed {bet_money} on {color}`")

    db.close()

  @betcash.error
  async def bet_cash_error(ctx, error):

    print(error)
    await ctx.send("Invalid format.")

  def num_players(self):

    num_players = 0

    for col in self.roulette:

      num_players += len(self.roulette[col])

    return num_players

  def num_winners(self):

    return len(self.roulette[self.color])

  def generate_result(self):

    number = random.randint(0, 37)

    if (
      (number == 0) or (number == 37)
    ):  # Number 37 is turned into 00, while both numbers will represent GREEN

      if number == 37:

        number = 00

      self.color = "GREEN"

    elif (number % 2) == 0:  # If it is even, it has landed on BLACK

      self.color = "BLACK"

    else:

      self.color = "RED"

    print(f"The result is: {self.color}, {number}")
    return [self.color, number]

  @commands.command("table")
  async def print_table(self, ctx):

    await ctx.send(roulette_table(self.roulette))

  @commands.command("startround")
  async def start_round(self, ctx):

    result = self.generate_result()

    prnt_result = roulette_results(self.return_winners(), self.return_losers())

    await ctx.send(
      f"```The result is a {result[0]} {result[1]}!\n{prnt_result[0]}{prnt_result[1]}```"
    )

    db = database(ctx.guild.id)

    if self.num_players() == 0:

      await ctx.send("`No one is betting right now.`")

    elif self.num_players() == 1:

      for player in self.roulette[result[0]]:

        db.change_bangers(self.roulette[result[0]][player] * 1.5, player)

    elif self.num_players() > 1:

      pot = 0

      for col in self.roulette:

        for player in self.roulette[col]:

          if col != self.color:

            pot += self.roulette[col][player]

      for col in self.roulette:

        for player in self.roulette[col]:

          if col == self.color:

            if len(self.roulette[col]) > 0:

              db.change_bangers(
                (pot // self.num_winners()) + self.roulette[col][player],
                player)

            else:

              await ctx.send("`No one won! Ya'll suck!`")

    db.add_query_roulette(self.color, int(result[1]))

    self.roulette = {"GREEN": {}, "BLACK": {}, "RED": {}}

  @start_round.error
  async def start_round_error(ctx, error):

    print(error)
    await ctx.send("`" + str(error) + "`")

  

  def return_winners(self):

    winners = {}

    for player in self.roulette[self.color]:

      winners[player] = self.roulette[self.color][player]

    return winners

  def return_losers(self):

    losers = {}

    for col in self.roulette:

      if (col != self.color):

        for player in self.roulette[col]:

          if player in losers.keys():

            losers[player] = +self.roulette[col][player]

          else:

            losers[player] = self.roulette[col][player]

    return losers

  def return_result(self):

    return [self.return_winners(), self.return_losers()]

  # def get_info(self, player):  # Depricated function. Ready for removal.

  #   return [
  #     player, self.players[player]["Money"], self.players[player]["Debt"]
  #   ]

  # def get_bettable(self):

  #   return self.roulette


async def setup(bot):

  await bot.add_cog(roulette(bot))
