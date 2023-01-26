""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import asyncpraw
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks

reddit_sorts = ["top", "hot", "rising", "controversial", "new"]

# Here we name the cog and create a new class for the cog.
class Reddit(commands.Cog, name="reddit"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="reddit",
        description="This is a testing command that does nothing.",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    # This will only allow owners of the bot to execute the command -> config.json
    @checks.is_owner()
    async def reddit(
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
            sub = await reddit.subreddit(subreddit, fetch=True)
            if (sub is not None):
                await ctx.send(f"Found the subreddit: {subreddit}")
                print(sub.display_name)
                print(sub.title)
                print(sub.description)
                if sort in reddit_sorts:
                    async for submission in getattr(sub, sort)(limit=num_posts):
                        await ctx.send(f'https://reddit.com/{submission.permalink}')
                else:
                    await ctx.send(f"Bad sort option.  Use --> {reddit_sorts}")
            else:
                await ctx.send(f"Can't find the subreddit: {subreddit}")


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Reddit(bot))
