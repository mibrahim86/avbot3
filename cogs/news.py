""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import json
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks
from newsapi import NewsApiClient

# Here we name the cog and create a new class for the cog.
class News(commands.Cog, name="news"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="news",
        description="Get the latest headlines using a search query.",
    )
    @checks.not_blacklisted()
    async def news(
        self,
        ctx: Context, 
        search_query: str,
        num_stories: int = 1
    ):
        #Initialize NewsApi
        newsapi = NewsApiClient(api_key=self.bot.config['NEWSAPI_TOKEN'])

        top_headlines = newsapi.get_top_headlines(q=search_query,
                                            sources='bbc-news, abc-news, al-jazeera-english, ars-technica, associated-press, axios, bbc-sport, bloomberg, cbc-news, cbs-news, buzzfeed, cnn, espn, fox-news, fox-sports, google-news, hacker-news, mashable, myv-news, nbc-news, newsweek, politico, reddit-r-all, techcrunch, the-globe-and-mail, the-washington-post, the-wall-street-journal, wired',
                                            language='en')
        print(top_headlines)                                      
        totalResults = top_headlines["totalResults"]
        count = 1
        if totalResults > 0:   
            await ctx.send(f'Total Headlines: {totalResults}')
            json_headlines = json.loads(json.dumps(top_headlines["articles"]))
            for h in json_headlines:
                print(h)
                await ctx.send(h["url"])
                count = count + 1
                if count > num_stories:
                    break
        else:
            await ctx.send(f"No headlines found for {search_query}")

        
    @commands.hybrid_command(
        name="headlines",
        description="Get the latest headlines by country.",
    )
    @checks.not_blacklisted()
    async def headlines(
        self,
        ctx: Context, 
        country: str = "us",
        num_stories: int = 1
    ):
        #Initialize NewsApi
        newsapi = NewsApiClient(api_key=self.bot.config['NEWSAPI_TOKEN'])

        top_headlines = newsapi.get_top_headlines(country=country)
                                            
        print(top_headlines)                                      
        totalResults = top_headlines["totalResults"]
        count = 1
        if totalResults > 0:   
            await ctx.send(f'Total Headlines: {totalResults}')
            json_headlines = json.loads(json.dumps(top_headlines["articles"]))
            for h in json_headlines:
                print(h)
                await ctx.send(h["url"])
                count = count + 1
                if count > num_stories:
                    break
        else:
            await ctx.send(f"No headlines found for {country}")

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(News(bot))
