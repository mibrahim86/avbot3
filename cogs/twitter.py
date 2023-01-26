""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import json
import tweepy
import discord
from discord.ext import commands
from discord.ext.commands import Context
from paginator import Paginator, Page, NavigationType
from helpers import checks

#Build WOEID Map
places_map = {}
woeid_file = open('database/woeid.json')
woeid_data = json.load(woeid_file)
places = woeid_data
for place in places:
    key = (place['name']).upper()
    value = place['woeid']
    places_map[key] = value
#print(places_map['UNITED STATES'])

# Here we name the cog and create a new class for the cog.
class Twitter(commands.Cog, name="twitter"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="twitter",
        description="Get twitter trends by location.",
    )
    @checks.not_blacklisted()
    async def twitter(
        self,
        ctx: Context,
        location: str = 'United States', 
        num_trends: int = 3
    ):
        auth = tweepy.OAuth2BearerHandler(self.bot.config["TWITTER_TOKEN"])
        api = tweepy.API(auth)
            
        count = 1
        if location.upper() in places_map:
            location_woeid = places_map[location.upper()]
            trends = api.get_place_trends(location_woeid)
            for t in trends:
                embed=discord.Embed(title="Twitter Trends", description=f"Getting the top {num_trends} trends from {location} on twitter!")
                for h in t["trends"]:          
                    print(h)
                    embed.add_field(name=f"{h['tweet_volume']} Tweets", value=f'[{h["name"]}]({h["url"]})', inline=True)
                    print(h['name'])
                    print(h['url'])
                    count = count + 1
                    if count > num_trends:
                        break
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Could not find place: {location}")
    @commands.hybrid_command(
        name="tweets",
        description="Get tweets by handle.",
    )
    @checks.not_blacklisted()
    async def tweets(
        self,
        ctx: Context,
        handle: str, 
        num_tweets: int = 3
    ):
        auth = tweepy.OAuth2BearerHandler(self.bot.config["TWITTER_TOKEN"])
        api = tweepy.API(auth)

        paginator = Paginator(self.bot)
        pages = []

        try: 
            tweets_list = api.user_timeline(screen_name=handle, count=num_tweets)
            await ctx.send(f"{handle} found")
            for tweet in tweets_list:
                #print(json.dumps(tweet._json, indent=4))
                print(tweet._json["text"])
                em = discord.Embed(title=handle, url=f"https://twitter.com/{handle}", description=tweet._json["text"])
                em.set_image(url=tweet._json["user"]["profile_image_url_https"])
                pages.append(Page(embed=em))        
                #await ctx.send(f"{tweet._json['text']}")
            await paginator.send(ctx.channel, pages, type=NavigationType.Buttons) 
        except Exception as e:
            print(e)
            await ctx.send(f"{handle} not found")

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Twitter(bot))
