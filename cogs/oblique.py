""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import datetime

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context
from pytz import timezone
from datetime import timedelta

from helpers import checks
from obliquestrategies import get_strategy

# Here we name the cog and create a new class for the cog.
class Oblique(commands.Cog, name="oblique"):
    def __init__(self, bot):
        print(f"initializing oblique")
        self.bot = bot
        self.send_strategy.start()

    @commands.hybrid_command(
        name="oblique",
        description="Get an oblique strategy.",
    )
    @checks.not_blacklisted()
    async def oblique(self, context: Context):
        embed=discord.Embed(title="Oblique Strategy", description=get_strategy())
        await context.send(embed=embed)

    #Tasks
    @tasks.loop(seconds=60)
    @checks.not_blacklisted()
    async def send_strategy(self):
        print("Start send_strategy()")
        channel = await self.bot.fetch_channel(self.bot.config['DISCORD_CHANNEL_ID'])
        self.bot.logger.info(f"Oblique Channel: {channel}")
        async for message in channel.history(limit=1):
            last_message_timestamp = message.created_at
            sixty_minutes_ago = datetime.now(timezone('UTC')) - timedelta(minutes=60)
            self.bot.info(f"Last message in {channel} was at {last_message_timestamp} by {message.author}")
            #print(sixty_minutes_ago)
            if last_message_timestamp < sixty_minutes_ago:
                await channel.send(f'`{get_strategy()}`')

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Oblique(bot))
