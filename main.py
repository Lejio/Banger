from discord.ext import commands
from datetime import datetime
import pytz
import discord
import os

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

cogs: list = ["features.random", "features.gbbs_database"]


@client.event
async def on_ready():

  print("Logged in successfully as: " + str(client.user))
  
  # await client.change_presence(status=discord.Status.online, activity=discord.Game(settings.BotStatus))
  for cog in cogs:
    try:
      
      print(f"Loading cog {cog}")
      await client.load_extension(cog)
      print(f"Loaded cog {cog}")
      
    except Exception as e:
      
      exc = "{}: {}".format(type(e).__name__, e)
      print("Failed to load cog {}\n{}".format(cog, exc))


def is_guild_owner():

  def predicate(ctx):
    return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id

  return commands.check(predicate)


@client.command("hello")
@commands.check_any(commands.is_owner(), is_guild_owner())
async def only_for_owners(ctx):
  await ctx.send('Hello mister owner!')


@only_for_owners.error
async def not_owner_error(ctx, error):

  await ctx.send("Bro you a imposter :angry:")


@client.command("bruh")  # Testing command
async def ping(ctx, ok):
  if ok == None:
    await ctx.send("Pong bruh")

  else:

    await ctx.send(f"Pong {ok}")


@ping.error
async def ping_error(ctx, error):  # Displays this if encounters and error

  if isinstance(error, commands.MissingRequiredArgument):

    await ctx.send("Wrong syntax.")

  else:

    await ctx.send("Bruh")


@client.command("racist?")
async def racist(ctx):
  await ctx.send("Yes")


@client.command("checkguild")
async def check_guild(ctx):

  guilds = ""

  for guild in client.guilds:

    guilds += f"{guild}: {guild.id}\n"

  await ctx.send(guilds)

@client.command("checkmembers")
async def check_members(ctx, guildid):

  members = ""

  for guild in client.guilds:

    if int(guild.id) == guildid:
      for member in guild.members:
  
        members += str(member) + "\n"
        await ctx.send(members)

      break

  else:

    await ctx.send("The entered guild is not a subscriber of this bot. (or you're just a retard and put in the wrong id)")


  


try:

  client.run(os.environ['TOKEN'])

except Exception:

  os.system("kill 1")

# import os
# import discord
# from dice_roll import random_generator
# from webserver import keep_alive
# from gambaling_game import roulette
# from check_user_string import check_user_string
# from printing import roulette_table, roulette_results
# # from lyricsbot import getsong

# if __name__ == "__main__":

#   intents = discord.Intents.all()  # Grants the bot access to all intents.
#   # intents.message_content = True
#   client = discord.Client(intents=intents)
#   roulette_game = roulette()  # Pre-creates roulette game.

#   roulette_active = False  # Boolean used to check if a roulette game is already active.

#   @client.event
#   async def on_ready():
#     print("We have logged on as {0.user}".format(client))
#     roulette_game = roulette()  # Pre-creates roulette game.
#     roulette_game.startgame(1000)

#   @client.event
#   async def on_message(message):

#     user_input = message.content.split()

#     user = str(message.author)

#     if (len(user_input) > 0):

#       user_input.pop(0)

#     if message.author == client.user:

#       return

#     elif message.content.startswith("!hello"):

#       if (len(message.content.split()) > 1):

#         user_name = ""
#         for i in user_input:

#           user_name = user_name + ' ' + i

#         print(user_name)

#         await message.channel.send("`Hello" + user_name +
#                                    " you're a fucking dumbass.`")

#       else:

#         await message.channel.send("Whats up bastard")

#     elif message.content.startswith("!rolldice"):

#       roll_check = check_user_string(user_input, True)

#       if (roll_check):

#         rand = random_generator(int(message.content.split()[1]))

#         await message.channel.send("`The result is: " + rand.roll_dice() + "`")

#       else:

#         await message.channel.send("`You can't roll a word brother.`")

#     elif message.content.startswith("!join"):

#       if (roulette_game.addplayer(user)):

#         await message.channel.send("`" + user + " joined the game.`")

#       else:

#         await message.channel.send("`" + user + " already joined.`")

#     elif message.content.startswith("!bet"):

#       if len(user_input) > 0:

#         if user_input[0].isdigit() and (user_input[1] == "BLACK"
#                                         or user_input[1] == "RED"
#                                         or user_input[1] == "GREEN"):

#           roulette_game.betcash(user, int(user_input[0]), user_input[1])

#           await message.channel.send("`" + user + " has placed " + user_input[0] +
#                                      " on " + user_input[1] + "`")
#         else:

#           await message.channel.send(
#             "```Invalid format. Please input after '!bet' the amount you want to bet followed by BLACK, RED, or GREEN```"
#           )

#       else:

#         await message.channel.send(
#           "```Invalid format. You are missing at least one parameter. Type '!help' for more information.```"
#         )

#     elif message.content.startswith("!startround"):

#       result = roulette_game.start_round()

#       await message.channel.send(result[0] + " " + str(result[1]) + "!")

#       if (roulette_game.end_round(result[0])):

#         prestr_result = roulette_game.return_result()

#         results = roulette_results(prestr_result[0], prestr_result[1])
#         await message.channel.send(results[0] + results[1])

#         roulette_game.roulette = {"GREEN": {}, "BLACK": {}, "RED": {}}

#       else:

#         roulette_game.roulette = {"GREEN": {}, "BLACK": {}, "RED": {}}
#         await message.channel.send("No one won! Y'all suck!")

#     elif message.content.startswith("!table"):

#       await message.channel.send("```" + roulette_table(roulette_game.get_bettable()) + "```")

#     elif message.content.startswith("!stats"):

#       info = roulette_game.get_info(user)

#       await message.channel.send("```" + info[0] + "\nCash: " + str(info[1]) +
#                                  "\nDebt: " + str(info[2]) + "```")

#     elif message.content.startswith("!"):

#       await message.channel.send(
#         "`Are you trying to use me big bro `:wink:`\nYou have inserted an invalid command.`"
#       )

#   keep_alive()

# try:

#   client.run(os.environ['TOKEN'])

# except Exception:

#   os.system("kill 1")
