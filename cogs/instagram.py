""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import discord
from discord.ext import commands
from discord.ext.commands import Context
from instagrapi import Client

from helpers import checks
from paginator import Paginator, Page, NavigationType

# Here we name the cog and create a new class for the cog.
class Instagram(commands.Cog, name="instagram"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="instagram",
        description="Get pictures from Instagram.",
    )
    @checks.not_blacklisted()
    async def instagram(
        self,
        ctx: Context,
        handle: str, 
        num_posts: int = 3
    ):
        await ctx.send(f"Loading {num_posts} most recent posts by {handle}...")
        cl = Client()
        paginator = Paginator(self.bot)
        pages = []

        IG_USERNAME = self.bot.config['ig_username']
        IG_PASSWORD = self.bot.config['ig_password']
        cl.login(IG_USERNAME, IG_PASSWORD)

        user_id = cl.user_id_from_username(handle)
        print(user_id)
        if user_id is not None:
            #await ctx.send(f"Found posts by {handle}")
            medias = cl.user_medias(user_id, num_posts)
            for m in medias:
                print(m.dict())
                if m.thumbnail_url is not None:
                    print(m.thumbnail_url)
                    em = discord.Embed(title=handle, url=f"https://instagram.com/{handle}", description=m.caption_text)
                    em.set_image(url=m.thumbnail_url)
                    pages.append(Page(embed=em))
                    #await ctx.send(m.thumbnail_url)
                    #await ctx.send(m.caption_text)
                else:
                    for r in m.resources:
                        print(r.thumbnail_url)
                        em = discord.Embed(title=handle, url=f"https://instagram.com/{handle}", description=m.caption_text)
                        em.set_image(url=r.thumbnail_url)
                        pages.append(Page(embed=em))
                        #await ctx.send(r.thumbnail_url)
                    #await ctx.send(m.caption_text)
            await paginator.send(ctx.channel, pages, type=NavigationType.Buttons)
        else:
            await ctx.send(f"Found no posts by {handle}")         



# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Instagram(bot))
