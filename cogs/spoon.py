""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import json
import requests
import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks
from paginator import Paginator, Page, NavigationType

# Here we name the cog and create a new class for the cog.
class Spoon(commands.Cog, name="spoon"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="recipe",
        description="This is a testing command that does nothing.",
    )
    @checks.not_blacklisted()
    async def recipe(self, context: Context, recipe_query: str, total_results: int = 3):
        search_url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch"
        id_query_string = {"query": recipe_query, "number": total_results}

        headers = {
        	"X-RapidAPI-Key": self.bot.config['RAPIDAPI_TOKEN'],
	        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }
        paginator = Paginator(self.bot)
        pages = []
        response = requests.request("GET", search_url, headers=headers, params=id_query_string)
        results = json.loads(response.text)['results']
        if results:
            await context.send(f"Found results for {recipe_query}")
            for result in results:
                print(result['id'])
                print(result['image'])

                info_query_string = {"includeNutrition":"true"}

                info_url = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{result['id']}/information"
                response = requests.request("GET", info_url, headers=headers, params=info_query_string)
                #print(response.text)
                info_results = json.loads(response.text)
                #print(info_results)
                #print(info_results['vegetarian'])
                print(info_results['title'])
                print(info_results['sourceUrl'])
                print(info_results['image'])
                print(info_results['instructions'])
                em = discord.Embed(title=info_results['title'], url=info_results['sourceUrl'], description=info_results['instructions'])
                em.set_image(url=info_results['image'])
                pages.append(Page(embed=em))
            await paginator.send(context.channel, pages, type=NavigationType.Buttons)
        else:
            await context.send(f"No results for {recipe_query}")

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Spoon(bot))
