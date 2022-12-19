import os
import discord
from dice_roll import random_generator
from webserver import keep_alive


intents = discord.Intents.all()
# intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print("We have logged on as {0.user}".format(client))

@client.event
async def on_message(message):

  if message.author == client.user:

    return

  elif message.content.startswith("!hello"):

    if (len(message.content.split()) > 1):
  
      user_input = message.content.split()
      user_input.pop(0)

      user_name = ""
      for i in user_input:
   
        user_name = user_name + ' '+ i

      print(user_name)
      
      await message.channel.send("Hello" + user_name + " you're a fucking dumbass.")

    else:

      await message.channel.send("Whats up bastard")

  elif message.content.startswith("!roastEvan"):

    await message.channel.send("You look like you eat rats for breakfast.")

  elif message.content.startswith("!rolldice"):

    rand = random_generator(int(message.content.split()[1]))
    rand_result = rand.roll_dice()

    await message.channel.send(rand_result)

keep_alive()

client.run(os.environ['TOKEN'])





  # @client.event
  # async def on_message(message):
  
  #   if message.author == client.user:
  
  #     return
  
  #   # print(f"{message.author} said {message.content} in the {message.channel} channel.")
  #   if message.content.startswith('+hello'):
  
  #     await message.channel.send('Hello dumbass')