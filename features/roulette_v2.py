import random
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import discord
from features.gbbs_database import database
from features.printing import *
import time


class roulette_v2(commands.Cog):

  def __init__(self, bot):

    # Single player is still broken.
    # It seems like if the one player puts bets on multiple colors, the lost money would still return to the user's pocket.

    self.bot = bot
    self.color = ""
    self.roulette = {
      "GREEN": {},
      "BLACK": {},
      "RED": {}
    }  


  @app_commands.command(name="bet", description="Places a bet on that respective color.")
  @app_commands.choices(choices=[app_commands.Choice(name="Black", value="BLACK"), app_commands.Choice(name="Red", value="RED"), app_commands.Choice(name="Green", value="GREEN")])
  async def betcash(self, interaction: discord.Interaction, bet_money:int, choices:app_commands.Choice[str]):

    db = database(interaction.guild_id)
    db.change_bangers(-int(bet_money), interaction.user.id)
    player = db.get_user(interaction.user.id)
    changing = False

    embed = discord.Embed(title=f"{str(interaction.user.display_name)}", description="Placing bet.", color=discord.Colour.yellow(), timestamp=datetime.utcnow())
    
    if (int(player[2]) < 0):

      db.change_bangers(int(bet_money), interaction.user.id)
      embed.add_field(name="Error", value="You have insufficient funds.")

      await interaction.response.send_message(embed=embed)

    else:

      if interaction.user in self.roulette[choices.value].keys():

        self.roulette[choices.value][interaction.user.id][1] += int(bet_money)
        embed.add_field(name="Raise!", value=f"{interaction.user.display_name} has placed {bet_money} more on {choices.value}")
        await interaction.response.send_message(embed=embed)

      else:

        for col in self.roulette:

          for player in self.roulette[col]:

            if (player == interaction.user.id):

              db.change_bangers(int(self.roulette[col][player][1]), interaction.user.id)
              self.roulette[col].pop(interaction.user.id)
              embed.add_field(name="Changing Bet!", value=f"{interaction.user.display_name} has placed {bet_money}$BNG on **{choices.value}**!")
              
              self.roulette[choices.value][interaction.user.id] = [interaction.user.display_name, int(bet_money)]
              await interaction.response.send_message(embed=embed)
              changing = True
              

        if not changing:

          self.roulette[choices.value][interaction.user.id] = [interaction.user.display_name, int(bet_money)]
          embed.add_field(name="New Bet!", value=f"{interaction.user.display_name} has placed {bet_money}$BNG on **{choices.value}**!")
          await interaction.response.send_message(embed=embed)
              


    db.close()

  

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

  @app_commands.command(name="table", description="This command allows you to view the current table.")
  async def print_table(self, interaction: discord.Interaction):

    prn_list = roulette_table(self.roulette)
    print(prn_list)
    embed = discord.Embed(title="Roulette Table", description="All current bets.", color=discord.Colour.yellow(), timestamp=datetime.utcnow())
    embed.add_field(name="Green", value=prn_list[0], inline=False)
    embed.add_field(name="Black", value=prn_list[1], inline=False)
    embed.add_field(name="Red", value=prn_list[2], inline=False)
    await interaction.response.send_message(embed=embed)
    

  @app_commands.command(name="startround", description="Starts the round. It would announce the winners and losers.")
  async def start_round(self, interaction: discord.Interaction):

    result = self.generate_result()

    prnt_result = roulette_results(self.return_winners(), self.return_losers())
    print(prnt_result)
    embed = discord.Embed(title="Roulette Result", description="The results are out!", color=discord.Colour.yellow(), timestamp=datetime.utcnow())
    embed.add_field(name="Winners:", value=prnt_result[0], inline=False)
    embed.add_field(name="Losers:", value=prnt_result[1], inline=False)

    await interaction.response.send_message(embed=embed)

    db = database(interaction.guild_id)

    if self.num_players() == 0:

      await interaction.response.send_message("`No one is betting right now.`")

    elif self.num_players() == 1:

      for player in self.roulette[result[0]]:

        db.change_bangers(self.roulette[result[0]][player][1] * 1.5, player)

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

              await interaction.response.send_message("`No one won! Ya'll suck!`")

    db.add_query_roulette(self.color, int(result[1]))

    self.roulette = {"GREEN": {}, "BLACK": {}, "RED": {}}

  @start_round.error
  async def start_round_error(interaction: discord.Interaction, error: Exception):

    print(error)
    await interaction.response.send_message("`" + str(error) + "`")

  

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


  # def get_players_table(color, interaction: discord.Interaction):

  #   table = ""
  #   for player in self.roulette[color]:

  #     table += f"{interaction.}"



async def setup(bot):

  await bot.add_cog(roulette_v2(bot))
