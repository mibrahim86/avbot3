""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import asyncpraw
import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
from helpers import checks

reddit_sorts = ["top", "hot", "rising", "controversial", "new"]

# Here we name the cog and create a new class for the cog.
class Reddit(commands.Cog, name="reddit"):
    def __init__(self, bot):
        self.bot = bot

    @checks.not_blacklisted()
    @app_commands.command(name="reddit", description="Return Reddit posts for a subreddit.")
    @app_commands.describe(sort='sort options on reddit')  
    @app_commands.choices(sort=[
        app_commands.Choice(name='top', value="top"),
        app_commands.Choice(name='hot', value="hot"),
        app_commands.Choice(name='controversial', value="controversial"),
        app_commands.Choice(name='rising', value="rising"),
        app_commands.Choice(name='new', value="new")
    ])
    async def reddit(
        self,
        interaction: discord.Interaction,
        subreddit: str,
        sort: app_commands.Choice[str],
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
                if sort.value in reddit_sorts:
                    all_embeds = []
                    async for submission in getattr(sub, sort.value)(limit=num_posts):
                        em = discord.Embed(title=submission.title, url=f'https://reddit.com/{submission.permalink}', description=submission.author)
                        all_embeds.append(em)
                    await interaction.response.send_message(embeds=all_embeds)
                else:
                    await interaction.response.send_message(f"Bad sort option.  Use --> {reddit_sorts}")
            except Exception as err:
                await interaction.response.send_message(f"Can't find the subreddit {subreddit}.")
                print(f"Unexpected {err=}, {type(err)=}")
                raise

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Reddit(bot))
