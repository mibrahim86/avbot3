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
import urllib.parse
from helpers import checks


# Here we name the cog and create a new class for the cog.
class Books(commands.Cog, name="books"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="books",
        description="Search the Google Books API.",
    )
    @checks.not_blacklisted()
    async def books(self, context: Context, search: str):
        base_url = "https://www.googleapis.com/books/v1/volumes"
        query_str = urllib.parse.quote_plus(search)
        params = {"q": search}
        response = requests.get(base_url, params=params)

        books_json = response.json()
        #await context.send(f"Searching...{search}")
        #print(json.dumps(books_json['items'], indent=4))
        first_book = books_json['items'][0]
        print(json.dumps(first_book, indent=4))

        title = first_book['volumeInfo']['title']
        authors = first_book['volumeInfo']['authors']
        description = first_book['volumeInfo']['description']
        preview_url = first_book['volumeInfo']['previewLink']
        image_url = first_book['volumeInfo']['imageLinks']['thumbnail']
        print(title)
        print(authors)
        print(description)
        print(preview_url)
        print(image_url)
        em = discord.Embed(title=title, url=preview_url, description=description)
        em.set_image(url=image_url)
        em.set_footer(text=authors)
        await context.send(embed=em)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Books(bot))
