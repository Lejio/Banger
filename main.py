from discord.ext import commands
from features.gbbs_database import database
from features.webserver import keep_alive
from datetime import datetime
import pytz
import discord
import os


client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
cogs: list = ["features.random", "features.roulette"]


@client.event
async def on_ready():
  """
    Client event. Runs when the bot is ready and has successfully logged in.
  """

  print("Logged in successfully as: " + str(client.user))

  for cog in cogs:  # Loads each config into the client.
    try:

      print(f"Loading cog {cog}")
      await client.load_extension(cog)
      print(f"Loaded cog {cog}")

    except Exception as e:  # Displays error if loading fails.

      exc = "{}: {}".format(type(e).__name__, e)
      print("Failed to load cog {}\n{}".format(cog, exc))


@client.event
async def on_member_join(member):
  """
    Under Construction. 
    Adds new users to the database.
  """

  print("Bruh" + str(member))
  

def is_guild_owner():
  """
    Determines if the current ctx is the guild owner and/or bot owner.
  """

  def predicate(ctx):
    return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id

  return commands.check(predicate)


@client.command("hello")
async def hello(ctx):
  """
    Test command. Echos back "Hello!".
  """
  await ctx.send('Hello!')


@hello.error
async def not_owner_error(ctx, error):
  """
    Test error. Should not happen anymore (if nothing major happens).
  """
  print(error)
  await ctx.send("Something is seriously wrong if this gets sent lol.")


@client.command("currentguild")
async def current_guild(ctx):
  """
    Outputs the current guild name and id if the user is in a guild.
  """

  if ctx.guild == None:

    await ctx.send("You are not in a server.")

  else:

    await ctx.send("The current server id is: " + str(ctx.guild.id))


@client.command("stats")
async def check_stats(ctx):
  """
    Checks the ctx.author's current stats. Including username, bangers, rank and level.
    All these information is retrieved via db connection.
  """

  db = database(ctx.guild.id, (client.get_guild(ctx.guild.id)).members)

  records = db.get_user(ctx.author)
  db.close()
  print(f"{ctx.author} retrieved data.")

  await ctx.send(
    f"User: {records[1]} ({records[0]})\nLevel: {records[2]}\nBangers: {records[3]}\nRank: {records[4]}"
  )

@check_stats.error
async def check_stats_error(ctx, error):
  """
    Prints and logs error if something happens.
  """

  print(error)
  await ctx.send(error)


@client.command("checkguilds")
@commands.check_any(commands.is_owner(), is_guild_owner())
async def check_guild(ctx):
  """
    Prints all the guilds the bot is currently apart of.
  """

  guilds = ""

  for guild in client.guilds:

    guilds += f"{guild}: {guild.id}\n"

  await ctx.send(guilds)


@client.command("checkmembers")
@commands.check_any(commands.is_owner(), is_guild_owner())
async def check_members(ctx):
  """
    Prints all the members in the current discord server.
  """

  members = ""
  guild = client.get_guild(ctx.guild.id)

  for member in guild.members:

    members += str(member) + "\n"

  await ctx.send(members)


@client.command("addmoney")
@commands.check_any(commands.is_owner(), is_guild_owner())
async def add_money(ctx, money, id):
  """
    Adds a specified amount of money into an account.
  """

  db = database(ctx.guild.id, (client.get_guild(ctx.guild.id)).members)

  db.change_bangers(int(money), id)
  db.close()
  await ctx.send(f"Added {money} to {id}")


@add_money.error
async def add_money_error(ctx, error):
  """
    Prints the error of add_money.
  """

  await ctx.send(str(error))
  print(str(error))

keep_alive()  # Webserver. This is pinged every 45 minutes to keep the bot alive.

"""
  Runs the bot. Sometimes it gets a TooManyRequests error. In which it would promptly kill the program and restart. (This is the only current known fix).
"""
try:

  client.run(os.environ['TOKEN'])

except Exception:

  os.system("kill 1")