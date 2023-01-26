""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import discord
from quote import quote
from discord.ext import commands
from discord.ext.commands import Context
from paginator import Paginator, Page, NavigationType

from helpers import checks


# Here we name the cog and create a new class for the cog.
class Goodreads(commands.Cog, name="goodreads"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="goodreads",
        description="Find quotes by authors."
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def goodreads(
        self,
        ctx: Context, 
        author_name: str,
        num_quotes: int = 3
    ):
        
        paginator = Paginator(self.bot)
        pages = []

        results = quote(author_name, limit=int(num_quotes))
        if len(results) > 0:
            await ctx.send(f"Found quotes for {author_name}")
            for r in results:
                print(r)
                goodreads_quote = r["quote"]
                author = r["author"]
                em=discord.Embed(title=author, description=goodreads_quote)
                pages.append(Page(embed=em))
            await paginator.send(ctx.channel, pages, type=NavigationType.Buttons)
        else:
            await ctx.send(f"No quotes found for {author_name}")


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Goodreads(bot))
