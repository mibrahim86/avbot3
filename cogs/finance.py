""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import json
import discord
import yfinance

from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks


# Here we name the cog and create a new class for the cog.
class Finance(commands.Cog, name="finance"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="stock",
        description="Get stock quote information.",
    )
    @checks.not_blacklisted()
    async def stock(
        self,
        ctx: Context, 
        ticker: str,
    ):
        s = yfinance.Ticker(ticker)
        print(s)
        if s is not None:
            print(s.info)
            if s.info['quoteType'] == "EQUITY":
                ask = "${:,.2f}".format(s.info["ask"])
                bid = "${:,.2f}".format(s.info["bid"])
                summary = s.info["longBusinessSummary"]
                embed=discord.Embed(title=f"{ticker}", url=f"https://cnbc.com/quotes/{ticker}",description=f"{summary}")
                embed.add_field(name=f"ASK", value=f"{ask}", inline=True)
                embed.add_field(name=f"BID", value=f"{bid}", inline=True)
                await ctx.send(embed=embed)
            elif s.info['quoteType'] == "ETF":
                ask = "${:,.2f}".format(s.info["ask"])
                bid = "${:,.2f}".format(s.info["bid"])
                summary = s.info['longBusinessSummary']
                embed=discord.Embed(title=f"{ticker}", url=f"https://cnbc.com/quotes/{ticker}",description=f"{summary}")
                embed.add_field(name=f"ASK", value=f"{ask}", inline=True)
                embed.add_field(name=f"BID", value=f"{bid}", inline=True)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"No information for {ticker}!")
        else:
            await ctx.send(f"No information for {ticker}!")


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Finance(bot))
