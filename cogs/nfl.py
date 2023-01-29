""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import json
import http.client
import discord
from discord.ext import commands
from discord.ext.commands import Context
from datetime import date
from helpers import checks


# Here we name the cog and create a new class for the cog.
class NFL(commands.Cog, name="nfl"):
    def __init__(self, bot):
        self.bot = bot
        self.nfl_headers = {
            'x-rapidapi-host': "v1.american-football.api-sports.io",
            'x-rapidapi-key': self.bot.config['SPORTS_TOKEN']
        }

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.hybrid_group(
        name="nfl",
        description="Get NFL information.",
    )
    async def nfl(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Please specify a subcommand.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @nfl.command(
        name="live",
        description="Get live NFL scores.",
    )
    @checks.not_blacklisted()
    async def nfl_live(self, ctx):
        nfl_conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")
        endpoint="games?live=all"
        nfl_conn.request("GET", "/"+endpoint, headers=self.nfl_headers)
        res = nfl_conn.getresponse()
        data = res.read()

        response = json.loads(data.decode("utf-8"))
        print(response)
        games = response["response"]
        if len(games) > 0:
            await ctx.send(f'{len(games)} games today.')
            for g in games:
                print(json.dumps(g, indent=4))
                team_json = g['teams']
                score_json = g['scores']
                status_json = g['game']
                periods_json = g['game'] 
                #print(json.dumps(team_json, indent=4))
                #print(json.dumps(score_json, indent=4))
                
                home_team = team_json['home']['name']
                away_team = team_json['away']['name']
                home_score = score_json['home']['total']
                away_score = score_json['away']['total']
                current_clock = status_json['status']['timer']
                current_quarter = periods_json['status']['short']

                #print(f'{home_team} ({home_score}) -- {away_team} ({away_score})')
                await ctx.send(f'```{home_team} ({home_score}) -- {away_team} ({away_score}) | Clock: {current_clock} Quarter: {current_quarter}```')
        else:
            await ctx.send('No live games right now!')
    
    @nfl.command(
        name="today",
        description="Get today's NFL games.",
    )
    @checks.not_blacklisted()
    async def nfl_today(self, ctx):
        
        nfl_conn = http.client.HTTPSConnection("v1.american-football.api-sports.io")
        endpoint="games?league=1&season=2022&date=" + str(date.today())
        nfl_conn.request("GET", "/"+endpoint, headers=self.nfl_headers)
        res = nfl_conn.getresponse()
        data = res.read()

        response = json.loads(data.decode("utf-8"))
        print(response)
        games = response["response"]
        if len(games) > 0:
            await ctx.send(f'{len(games)} games today.')
            for g in games:
                print(json.dumps(g, indent=4))
                team_json = g['teams']
                score_json = g['scores']
                status_json = g['game']
                periods_json = g['game'] 
                #print(json.dumps(team_json, indent=4))
                #print(json.dumps(score_json, indent=4))
                
                home_team = team_json['home']['name']
                away_team = team_json['away']['name']
                home_score = score_json['home']['total']
                away_score = score_json['away']['total']
                current_clock = status_json['status']['timer']
                current_quarter = periods_json['status']['short']

                #print(f'{home_team} ({home_score}) -- {away_team} ({away_score})')
                await ctx.send(f'```{home_team} ({home_score}) -- {away_team} ({away_score}) | Clock: {current_clock} Quarter: {current_quarter}```')
        else:
            await ctx.send('No games today!')        


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(NFL(bot))
