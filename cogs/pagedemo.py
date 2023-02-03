""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed

from helpers import checks

from paginator import Paginator, Page, NavigationType



# Here we name the cog and create a new class for the cog.
class PageDemo(commands.Cog, name="pagedemo"):
    def __init__(self, bot):
        self.bot = bot
        
    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="pages",
        description="This is a testing command that does nothing.",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    # This will only allow owners of the bot to execute the command -> config.json
    @checks.is_owner()
    async def pages(self, context: Context):
        paginator = Paginator(self.bot)
        
        pages = [
            Page(content="Click!", embed=Embed(title="Page #1", description="Testing")),
            Page(embed=Embed(title="Page #2", description="Still testing")),
            Page(embed=Embed(title="Page #3", description="Guess... testing"))
        ]

        await paginator.send(context.channel, pages, type=NavigationType.Buttons)
    
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    # This will only allow owners of the bot to execute the command -> config.json
    @checks.is_owner()
    @app_commands.command()
    @app_commands.describe(fruits='fruits to choose from')
    @app_commands.choices(fruits=[
        app_commands.Choice(name='apple', value=1),
        app_commands.Choice(name='banana', value=2),
        app_commands.Choice(name='cherry', value=3),
    ])
    async def fruit(self, interaction: discord.Interaction, fruits: app_commands.Choice[int]):
        await interaction.response.send_message(f'Your favourite fruit is {fruits.name}.')


    @commands.command()
    async def listcommands(self,ctx):
        commands = [c.name for c in self.bot.commands]
        print(commands)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(PageDemo(bot))
