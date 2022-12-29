from discord import app_commands
from discord.ext import commands
import discord

class test(commands.Cog):

  @app_commands.command(name="test", description="Test Command")
  async def test_1(self, interaction: discord.Interaction, name: str):
    print(type(interaction))
    await interaction.response.send_message(f"Hello {name}")

async def setup(bot):

  await bot.add_cog(test(bot))


