""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import random
import discord
from discord.ext import commands
from discord.ext.commands import Context

from tinydb import TinyDB, Query
from helpers import checks


#List of regulars
regs = ['avdrav', 'aya', 'dol', 'robot', 'toc', 'virtue', 'starsmash', 'ina', 'crash', 'quin', 'soupy']

#Initialize DB
db = TinyDB('database/quotes.json')

# Here we name the cog and create a new class for the cog.
class Quote(commands.Cog, name="quote"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @checks.not_blacklisted()  
    @commands.hybrid_command(name="regulars", description="Avscord Regulars") 
    async def regulars(self, context: Context):
        embed=discord.Embed(title="Avscord Regulars", description="Frequent visitors get quotes!")
        for r in regs:
            embed.add_field(name=r, value="", inline=False)
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="addquote",
        description="Add a quote by a regular"
    )
    @checks.not_blacklisted()
    async def addquote(
        self,
        ctx: Context, 
        regular: str,
        quote: str
    ):
        if regular in regs:
            db.insert({'name': regular, 'quote': quote })
            embed=discord.Embed(title=regular, description=f"{regular}'s quote was added!")
        else:
            embed=discord.Embed(title=regular, description=f"{regular}'s is not a regular!")
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="getquote",
        description="Get a quote by a regular"
    )
    @checks.not_blacklisted()
    async def getquote(
        self,
        ctx: Context, 
        regular: str
    ):
        if regular in regs:
            Quote = Query()
            results = db.search(Quote.name == regular)
            q = random.choice(results)
            embed=discord.Embed(title=q['name'], description=q['quote'])
        else:
            embed=discord.Embed(title="Nope!", description=f"{regular} is not a regular!")
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="getallquotes",
        description="Get all quotes by a regular"
    )
    @checks.not_blacklisted()
    async def getallquotes(
        self,
        ctx: Context, 
        regular: str
    ):
        if regular in regs:
            Quote = Query()
            results = db.search(Quote.name == regular)
            embed = discord.Embed(title=regular, description="")
            for r in results:
                embed.add_field(name=f"", value=f"{r['quote']}", inline=False)
        else:
            embed=discord.Embed(title="Nope!", description=f"{regular} is not a regular!")
        await ctx.send(embed=embed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Quote(bot))
