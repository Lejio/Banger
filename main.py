from discord.ext import commands
from discord import app_commands
from under_construction.test_v2 import test
import discord
from features.gbbs_database import database
from features.webserver import keep_alive
from datetime import datetime
import pytz
import os


client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
# cogs: list = ["features.random", "features.roulette_v1"]
cogs: list = ["under_construction.test_v2", "features.roulette_v2", "features.random_v2"]


@client.event
async def on_ready():
  """
    Client event. Runs when the bot is ready and has successfully logged in.
  """

  print(f"\n{datetime.utcnow()}: Logged in successfully as: " + str(client.user) + "\n")

  for cog in cogs:  # Loads each config into the client.
    # try:

    await client.load_extension(cog)
    print(f"Loaded cog {cog}")

  print("Successfully loaded all Cogs\n")

    # except Exception as e:  # Displays error if loading fails.

    # exc = "{}: {}".format(type(e).__name__, e)
    # print("Failed to load cog {}\n{}".format(cog, exc))
      
  synced = await client.tree.sync()
  print(f"Synced {len(synced)} commands.")
  

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


@client.tree.command(name="hello", description="A hello echoer.")
async def hello(interaction: discord.Interaction, member: discord.Member):
  """
    Test command. Echos back "Hello!".
  """
  embed = discord.Embed(title="test", description=f"{str(member)} said hello!", color=discord.Colour.yellow(), timestamp=datetime.utcnow())
  embed.add_field(name="bruh", value="yes")
  await interaction.response.send_message(embed=embed)


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

def get_user_id(members):
  member_ids = []
  for member in members:

    member_ids.append(member.id)

  return member_ids
  
@client.tree.command(name="stats", description="View the your own stats or other member's.")
async def check_stats(interaction: discord.Interaction, member: discord.Member=None):
  """
    Checks the ctx.author's current stats. Including username, bangers, rank and level.
    All these information is retrieved via db connection.
  """
  if member == None:

    member = interaction.user

  db = database(interaction.guild_id, (get_user_id(client.get_guild((interaction.guild_id)).members)))
  print(interaction.user.id)
  records = db.get_user(member.id)
  print(records)
  db.close()

  embed = discord.Embed(title=f"{member.display_name}", description="The current stats:", 
                        color=discord.Colour.yellow(),
                        timestamp=datetime.utcnow())
  embed.set_thumbnail(url=member.avatar)
  embed.add_field(name="User ID", value=f"{member.id}")
  embed.add_field(name="Level", value=f"{records[1]}")
  embed.add_field(name="$B", value=f"{records[2]}", inline=False)
  # embed.add_field(name="Rank", value=)
  embed.add_field(name="Highest Role", value=f"{member.top_role.mention}")

  print(f"{interaction.user} retrieved data.")

  await interaction.response.send_message(embed=embed)
  embed.clear_fields()


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
  await ctx.send(f"`Added {money} to {id}`")


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