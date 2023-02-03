""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import imdb
import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks
from paginator import Paginator, Page, NavigationType

# Here we name the cog and create a new class for the cog.
class IMDB(commands.Cog, name="imdb"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="imdb",
        description="Search IMDB for a movie.",
    )
    @checks.not_blacklisted()
    async def imdb(
        self, 
        context: Context,
        movie_name: str,
        num_results: int = 3
    ):
        ia = imdb.Cinemagoer()
        paginator = Paginator(self.bot)
        pages = []

        movies = ia.search_movie(movie_name)
        count = 1
        await context.send(f"Found {movie_name}!")
        for m in movies:
            em = discord.Embed(title=f"{m}", url=f"https://imdb.com/title/tt{m.getID()}", description="")
            em.set_image(url=m.get_fullsizeURL())
            pages.append(Page(embed=em))
            count = count + 1
            if count > num_results:
                break
        await paginator.send(context.channel, pages, type=NavigationType.Buttons)

    @commands.hybrid_command(
        name="actor",
        description="Search IMDB for an actor.",
    )
    @checks.not_blacklisted()
    async def actor(
        self, 
        context: Context,
        actor_name: str,
        num_results: int = 3
    ):
        ia = imdb.Cinemagoer()
        paginator = Paginator(self.bot)
        pages = []

        actors = ia.search_person(actor_name)
        count = 1
        await context.send(f"Found {actor_name}!")
        for a in actors:
            em = discord.Embed(title=f"{a}", url=f"https://imdb.com/name/nm{a.getID()}", description="")
            em.set_image(url=a.get_fullsizeURL())
            pages.append(Page(embed=em))
            count = count + 1
            if count > num_results:
                break
        await paginator.send(context.channel, pages, type=NavigationType.Buttons)

        


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(IMDB(bot))
 