""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import imdb
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks


# Here we name the cog and create a new class for the cog.
class IMDB(commands.Cog, name="imdb"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="movie",
        description="Search IMDB for a movie.",
    )
    @checks.not_blacklisted()
    async def movie(self, context: Context):
        ia = imdb.Cinemagoer()
        movies = ia.search_movie('matrix')
        for m in movies:
            print(f"{m}")
            print(f"{m.get_fullsizeURL()}")

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(IMDB(bot))
