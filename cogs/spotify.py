""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import json
import discord
import spotipy
from discord.ext import commands
from discord.ext.commands import Context
from spotipy.oauth2 import SpotifyClientCredentials
from helpers import checks
from paginator import Paginator, Page, NavigationType


# Here we name the cog and create a new class for the cog.
class Spotify(commands.Cog, name="spotify"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="spotify",
        description="Get tops songs by an artist from Spotify",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def spotify(self, ctx, artist_name="Radiohead", limit_arg=10):

        #Initialize Spotify
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=self.bot.config["spotipy_client_id"],
                                                           client_secret=self.bot.config["spotipy_client_secret"]))

        paginator = Paginator(self.bot)
        pages = []

        results = sp.search(q='artist:'+artist_name, type='artist')
        #print(json.dumps(results, indent=4))
        items = results['artists']['items']
        artist_uri = ""
        if len(items) > 0:
            artist_uri = items[0]['uri']
            artist_name = items[0]['name']
            print(artist_name+"="+artist_uri)
        if artist_uri != "":
            top_tracks = sp.artist_top_tracks(artist_uri)
            for track in top_tracks['tracks'][:limit_arg]:
                track_name = track['name']
                audio = track['external_urls']['spotify']
                cover_art = track['album']['images'][0]['url']
                
                embed=discord.Embed(title=track_name, url=audio, description=artist_name)
                embed.set_image(url=cover_art)
                pages.append(Page(embed=embed))
            await paginator.send(ctx.channel, pages, type=NavigationType.Buttons)
        else:
            await ctx.send(f"{artist_name} not found!")

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Spotify(bot))
