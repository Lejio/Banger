import discord
from discord.ext import commands
import youtube_dl


class music_bot(commands.Cog):

  def __init__(self, client):

    self.client = client

  @commands.command()
  async def join(self, ctx):

    if ctx.author.voice is None:

      await ctx.send(
        f"{ctx.author} are you dumb? You gotta be in a voice channel to use me."
      )

    voice_channel = ctx.author.voice.channel

    if ctx.client is None:

      await voice_channel.connect()

    else:

      ctx.voice_client.move_to(voice_channel)

  @commands.command()
  async def disconnect(self, ctx):

    await ctx.voice_client.disconnect()

  @commands.command()
  async def play(self, ctx, url):

    ctx.voice_client.stop()
    FFMPEG_OPTIONS = {
      'before_options':
      '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
      'options': '-vn'
    }
    YDL_OPTIONS = {'format': 'bestaudio'}

    vc = ctx.voice_client

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:

      info = ydl.extract_info(url, download=False)

      url2 = info['formats'][0]['url']

      source = await discord.FFmpedOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)

      vc.play(source)

  @commands.command()
  async def pause(self, ctx):

    await ctx.voice_client.pause()
    await ctx.send("The music has been paused.")

  @commands.command()
  async def resume(self, ctx):

    await ctx.voice_client.resume()
    await ctx.send("The music has been resumed.")

  @commands.command(name="sayhello")
  async def sayhello(self, message):

    if message.author == self.client.user:

      return

    else:

      await message.channel.send("bruh what the fuck yiou want")


def setup(client):

  client.add_cog(music_bot(client))
