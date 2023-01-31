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
from paginator import Paginator, Page, NavigationType


# Here we name the cog and create a new class for the cog.
class Books(commands.Cog, name="books"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="book",
        description="Search the Google Books API by keyword.",
    )
    @checks.not_blacklisted()
    async def book(self, context: Context, search: str):
        base_url = "https://www.googleapis.com/books/v1/volumes"
        query_str = urllib.parse.quote_plus(search)
        params = {"q": search}
        response = requests.get(base_url, params=params)

        paginator = Paginator(self.bot)
        pages = []

        books_json = response.json()
        #await context.send(f"Searching...{search}")
        #print(json.dumps(books_json['items'], indent=4))
        #first_book = books_json['items'][0]
        #print(json.dumps(first_book, indent=4))

        try:
            for book in books_json['items']: 
                title = book['volumeInfo']['title']
                preview_url = book['volumeInfo']['previewLink']
                
                if 'authors' not in book['volumeInfo']:
                    authors = ""
                else:
                    authors = book['volumeInfo']['authors']
                authors = book['volumeInfo']['authors']
                
                if 'description' not in book['volumeInfo']:
                    description = ""
                else:
                    description = book['volumeInfo']['description']

                if 'imageLinks' not in book['volumeInfo']:
                    image_url = ""
                else:
                    image_url = book['volumeInfo']['imageLinks']['thumbnail']
                
                print(title)
                print(authors)
                print(description)
                print(preview_url)
                print(image_url)
                
                em = discord.Embed(title=title, url=preview_url, description=description)
                em.set_image(url=image_url)
                em.set_footer(text=authors)
                pages.append(Page(embed=em))
            await paginator.send(context.channel, pages, type=NavigationType.Buttons)
        except Exception as err:
            await context.send(f"Can't find {search}.")
            print(f"Unexpected {err=}, {type(err)=}")
            raise


    @commands.hybrid_command(
        name="author",
        description="Search the Google Books API by author.",
    )
    @checks.not_blacklisted()
    async def author(self, context: Context, search: str, num_books: int = 3):
        base_url = "https://www.googleapis.com/books/v1/volumes"
        #query_str = urllib.parse.quote_plus(search)
        params = {"q": f"inauthor:{search}"}
        response = requests.get(base_url, params=params)

        paginator = Paginator(self.bot)
        pages = []

        books_json = response.json()
        #await context.send(f"Searching...{search}")
        #print(json.dumps(books_json['items'], indent=4))
        #first_book = books_json['items'][0]
        #print(json.dumps(first_book, indent=4))

        try:
            for book in books_json['items']:
                title = book['volumeInfo']['title']
                authors = book['volumeInfo']['authors']
                if 'description' not in book['volumeInfo']:
                    description = ""
                else:
                    description = book['volumeInfo']['description']
                preview_url = book['volumeInfo']['previewLink']
                image_url = book['volumeInfo']['imageLinks']['thumbnail']
                print(title)
                print(authors)
                print(description)
                print(preview_url)
                print(image_url)
                em = discord.Embed(title=title, url=preview_url, description=description)
                em.set_image(url=image_url)
                em.set_footer(text=authors)
                pages.append(Page(embed=em))
            await paginator.send(context.channel, pages, type=NavigationType.Buttons)
        except Exception as err:
            await context.send(f"Can't find {search}.")
            print(f"Unexpected {err=}, {type(err)=}")
            raise

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Books(bot))
