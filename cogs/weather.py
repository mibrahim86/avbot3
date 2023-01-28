""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import requests
import discord
import urllib.parse
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks


# Here we name the cog and create a new class for the cog.
class Weather(commands.Cog, name="weather"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="weather",
        description="This is a testing command that does nothing.",
    )
    @checks.not_blacklisted()
    async def weather(self, context: Context, city: str = 'Philadelphia'):
        city_url = urllib.parse.quote_plus(city)
        image_url = f"https://wttr.in/{city_url}.png"
        print(image_url)
        #response = requests.get(image_url)
        em = discord.Embed(title="Weather", description=city)
        em.set_image(url=image_url)
        await context.send(embed=em)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Weather(bot))
