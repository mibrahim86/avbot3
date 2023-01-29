""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import requests
import json
import discord
from discord.ext import commands
from discord.ext.commands import Context
from paginator import Paginator, Page, NavigationType
from helpers import checks


# Here we name the cog and create a new class for the cog.
class Urban(commands.Cog, name="urban"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="urban",
        description="This is a testing command that does nothing.",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def urban(self, context: Context, term: str):
        
        paginator = Paginator(self.bot)
        pages = []
      
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        querystring = {"term": term}
        headers = {
	        "X-RapidAPI-Key": self.bot.cofig['URBAN_DICTIONARY_TOKEN'],
	        "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        definitions = json.loads(response.text)

        print(json.dumps(definitions['list']))
        for definition in definitions['list']:
            print(definition['definition'])
            print(definition['permalink'])
            print(definition['example'])
            em = discord.Embed(title=term, description=definition['definition'])
            em.add_field(name="Example", value=definition['example'])
            em.set_footer(text=f"Upvotes({definition['thumbs_up']}) |  Downvotes({definition['thumbs_down']})")
            pages.append(Page(embed=em))
        await paginator.send(context.channel, pages, type=NavigationType.Buttons)
             

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Urban(bot))
