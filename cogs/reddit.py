""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import praw
import asyncpraw
import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
from helpers import checks
from paginator import Paginator, Page, NavigationType

reddit_sorts = ["top", "hot", "rising", "controversial", "new"]

# Here we name the cog and create a new class for the cog.
class Reddit(commands.Cog, name="reddit"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(
        name="redditasync",
        description="Search Reddit Async",
    )
    @checks.not_blacklisted()
    async def redditasync(
        self,
        ctx: Context,
        subreddit: str,
        sort: str,
        num_posts: int = 1
    ):
        async with asyncpraw.Reddit(
            client_id=self.bot.config['REDDIT_CLIENT_ID'],
            client_secret=self.bot.config['REDDIT_CLIENT_SECRET'],
            user_agent="avbot user agent"
        ) as reddit:
            try:
                sub = await reddit.subreddit(subreddit, fetch=True)
                print(sub)  
                if sort in reddit_sorts:
                    all_embeds = []
                    async for submission in getattr(sub, sort)(limit=num_posts):
                        em = discord.Embed(title=submission.title, url=f'https://reddit.com/{submission.permalink}', description=submission.author)
                        all_embeds.append(em)
                    await ctx.send(embeds=all_embeds)
                else:
                    await ctx.send(f"Bad sort option.  Use --> {reddit_sorts}")
            except Exception as err:
                await ctx.send(f"Can't find the subreddit {subreddit}.")
                print(f"Unexpected {err=}, {type(err)=}")
                raise

    @commands.hybrid_command(
        name="reddit",
        description="Search Reddit",
    )
    @checks.not_blacklisted()
    async def reddit(
        self,
        ctx: Context,
        subreddit: str,
        sort: str,
        num_posts: int = 1
    ):
        paginator = Paginator(self.bot)
        pages = []
        
        reddit = praw.Reddit(
            client_id=self.bot.config['REDDIT_CLIENT_ID'],
            client_secret=self.bot.config['REDDIT_CLIENT_SECRET'],
            user_agent="avbot user agent"
        )

        try:
            all_embeds = []
            
            if sort == "top":
                submissions = reddit.subreddit(subreddit).top(limit=num_posts)
            elif sort == "hot":
                submissions = reddit.subreddit(subreddit).hot(limit=num_posts)
            elif sort == "rising":
                submissions = reddit.subreddit(subreddit).rising(limit=num_posts)
            elif sort == "controversial":
                submissions = reddit.subreddit(subreddit).controversial(limit=num_posts)
            elif sort == "new":
                submissions = reddit.subreddit(subreddit).new(limit=num_posts)
            else:
                submissions = []    

            if submissions != []:
                await ctx.send(f"Found the {subreddit} subreddit")
                for submission in submissions:
                    print(submission.title)
                    em = discord.Embed(title=submission.title, url=f'https://reddit.com/{submission.permalink}', description=submission.author)
                    all_embeds.append(em)
                    pages.append(Page(embed=em))
                await paginator.send(ctx.channel, pages, type=NavigationType.Buttons)
            else:
                await ctx.send(f"Bad Sort. Use {reddit_sorts}")
        except Exception as err:
            await ctx.send(f"Can't find the subreddit {subreddit}.")
            print(f"Unexpected {err=}, {type(err)=}")
            raise

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Reddit(bot))
