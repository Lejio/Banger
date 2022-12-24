import os
import discord
from dice_roll import random_generator
from webserver import keep_alive
from gambaling_game import create_roulette
from check_user_string import check_user_string
from printing import roulette_table, roulette_results
# from lyricsbot import getsong

if __name__ == "__main__":

  intents = discord.Intents.all()  # Grants the bot access to all intents.
  # intents.message_content = True
  client = discord.Client(intents=intents)
  roulette_game = create_roulette()  # Pre-creates roulette game.

  roulette_active = False  # Boolean used to check if a roulette game is already active.

  @client.event
  async def on_ready():
    print("We have logged on as {0.user}".format(client))
    roulette_game = create_roulette()  # Pre-creates roulette game.
    roulette_game.startgame(1000)

  @client.event
  async def on_message(message):

    user_input = message.content.split()

    user = str(message.author)

    if (len(user_input) > 0):

      user_input.pop(0)

    if message.author == client.user:

      return

    elif message.content.startswith("!hello"):

      if (len(message.content.split()) > 1):

        user_name = ""
        for i in user_input:

          user_name = user_name + ' ' + i

        print(user_name)

        await message.channel.send("Hello" + user_name +
                                   " you're a fucking dumbass.")

      else:

        await message.channel.send("Whats up bastard")

    elif message.content.startswith("!rolldice"):

      roll_check = check_user_string(user_input, True)

      if (roll_check):

        rand = random_generator(int(message.content.split()[1]))

        await message.channel.send(rand.roll_dice())

      else:

        await message.channel.send("You can't roll a word brother.")

    # elif message.content.startswith("!runroulette"):
    #   if roulette_game_active:

    #     await message.channel.send("Roulette game has started!")
    #     roulette_game_active = False

    #   else:

    #     await message.channel.send("A roulette game is already in play.")

    elif message.content.startswith("!addplayer"):

      if (roulette_game.addplayer(user)):

        await message.channel.send(user + " joined the game")

      else:

        await message.channel.send(user + " already joined.")

    elif message.content.startswith("!bet"):

      if len(user_input) > 0:

        if user_input[0].isdigit() and (user_input[1] == "BLACK"
                                        or user_input[1] == "RED"
                                        or user_input[1] == "GREEN"):

          roulette_game.betcash(user, int(user_input[0]), user_input[1])

          await message.channel.send(user + " has placed " + user_input[0] +
                                     " on " + user_input[1])
        else:

          await message.channel.send(
            "Invalid format. Please input after '!bet' the amount you want to bet followed by BLACK, RED, or GREEN"
          )

      else:

        await message.channel.send(
          "Invalid format. You are missing at least one parameter. Type '!help' for more information."
        )

    elif message.content.startswith("!startround"):

      result = roulette_game.start_round()

      await message.channel.send(result[0] + " " + str(result[1]) + "!")

      if (roulette_game.end_round(result[0])):

        prestr_result = roulette_game.return_result()

        results = roulette_results(prestr_result[0], prestr_result[1])
        await message.channel.send(results[0] + results[1])

        roulette_game.roulette = {"GREEN": {}, "BLACK": {}, "RED": {}}

      else:

        roulette_game.roulette = {"GREEN": {}, "BLACK": {}, "RED": {}}
        await message.channel.send("No one won! Y'all suck!")

    elif message.content.startswith("!table"):

      await message.channel.send(roulette_table(roulette_game.get_bettable()))

    elif message.content.startswith("!stats"):

      info = roulette_game.get_info(user)

      await message.channel.send(info[0] + "\nCash: " + str(info[1]) +
                                 "\nDebt: " + str(info[2]))

    elif message.content.startswith("!"):

      await message.channel.send("`Are you trying to use me big bro `:wink:`\nYou have inserted an invalid command.`")

    # elif message.content.startswith("!searchlyrics"):

    #   song = ""

    #   for i in range(len(user_input)):

    #     song += user_input[i] + " "

    #   lyrics = getsong(user_input)

    #   await message.channel.send(lyrics)

  keep_alive()

try:

  client.run(os.environ['TOKEN'])

except Exception:

  os.system("kill 1")
