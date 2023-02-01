""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import random
import json
import pytumblr
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks


# Here we name the cog and create a new class for the cog.
class Tumblr(commands.Cog, name="tumblr"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="tumblr",
        description="Get random tumblr posts.",
    )
    @checks.not_blacklisted()

    async def tumblr(
        self,
        ctx: Context, 
        tumblr_blog: str,
        num_stories: int = 1
    ):
        #Initialize Tumblr
        tum = pytumblr.TumblrRestClient(
            self.bot.config['TUMBLR_CLIENT_ID'],
            self.bot.config['TUMBLR_CLIENT_SECRET'],
            self.bot.config['TUMBLR_TOKEN'],
            self.bot.config['TUMBLR_TOKEN_SECRET']
        )

        try:
            blog_info = tum.blog_info(tumblr_blog)
            #print(json.dumps(blog_info, indent=4))
            total_posts = blog_info['blog']['total_posts']
            if total_posts > 0:
                #await ctx.send(f"Found blog: {tumblr_blog}")
                posts_json = tum.posts(tumblr_blog, limit=num_stories, offset=random.randint(1,total_posts), type="photo")
                #print(json.dumps(posts_json['posts'], indent=4))
                for post in posts_json['posts']:
                    print(json.dumps(post, indent=4))
                    image_url = post['post_url']
                    await ctx.send(f"{image_url}")
            else:
                await ctx.send(f"Can't find the blog: {tumblr_blog}")
        except Exception as err:
            await ctx.send(f"Can't find the blog {tumblr_blog}.")
            print(f"Unexpected {err=}, {type(err)=}")
            raise      

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Tumblr(bot))
