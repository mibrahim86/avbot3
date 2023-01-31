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

from helpers import checks
from paginator import Paginator, Page, NavigationType

# Here we name the cog and create a new class for the cog.
class Scores(commands.Cog, name="scores"):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = self.bot.config['ODDS_TOKEN']
        self.api_base_url = "https://api.the-odds-api.com/v4/sports/"
        self.leagues = {
            'nfl': 'americanfootball_nfl',
            'nba': 'basketball_nba',
            'ncaab': 'basketball_ncaab',
            'mlb': 'baseball_mlb',
            'cricket': 'cricket_test_match',
            'nhl' : 'icehockey_nhl',
            'ncaaf': 'americanfootball_ncaaf'
        }

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.hybrid_command(
        name="scores",
        description="Get sports scores.",
    )
    @checks.not_blacklisted()
    async def scores(self, context: Context, league: str = "nfl", days_from: int = 1):
 
        paginator = Paginator(self.bot)
        pages = []
 
        if league in self.leagues:
            full_league = self.leagues[league]
            full_url = f"{self.api_base_url}/{full_league}/scores"
            print(full_url)
            sports_response = requests.get(full_url, params = {
                'api_key': self.api_key,
                'daysFrom': days_from
            })
            print(sports_response)
            sports_json = json.loads(sports_response.text)
            if sports_json is None:
                await context.send('There was a problem with the sports request:', sports_json['msg'])
            else:
                print(json.dumps(sports_json, indent=4))
                home_score = 0
                away_score = 0
                if len(sports_json) > 0:
                    await context.send(f"Found {len(sports_json)} games.")
                    for game in sports_json:
                        home_team = game['home_team']
                        away_team = game['away_team']
                        commence_time = game['commence_time']
                        scores = game['scores']
                        if scores is not None:
                            for s in scores:
                                if s['name'] == home_team:
                                    home_score = s['score']
                                elif s['name'] == away_team:
                                    away_score = s['score']
                            em = discord.Embed(title=f"{league} scores", description=f"Home Team: {home_team} ({home_score})\nAway Team {away_team} ({away_score})")
                            em.set_footer(text=f"Start time: {commence_time}")
                            pages.append(Page(embed=em))
                    if pages:
                        await paginator.send(context.channel, pages, type=NavigationType.Buttons)
                    else:
                        await context.send(f"No scores in the {league} today.")
                else:
                    await context.send(f'{league} has no games.')
        else:
            await context.send(f"{league} is not a valid league!")

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Scores(bot))
