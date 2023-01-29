""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import json
import discord
import http.client
from discord.ext import commands
from discord.ext.commands import Context
from datetime import date
from helpers import checks
from urllib.parse import quote



# Here we name the cog and create a new class for the cog.
class NBA(commands.Cog, name="nba"):
    def __init__(self, bot):
        self.bot = bot
        self.nba_headers = {
            'x-rapidapi-host': "v2.nba.api-sports.io",
            'x-rapidapi-key': self.bot.config['SPORTS_TOKEN']
        }

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    
    @commands.hybrid_group(
        name="nba",
        description="Get NBA information.",
    )
    @checks.not_blacklisted()
    async def nba(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Please specify a subcommand.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
    
    @nba.command(
        name="live",
        description="Get live NBA scores.",
    )
    @checks.not_blacklisted()
    async def nba_live(self, ctx: Context):
        nba_conn = http.client.HTTPSConnection("v2.nba.api-sports.io")
        endpoint="games?live=all"
        nba_conn.request("GET", "/"+endpoint, headers=self.nba_headers)
        res = nba_conn.getresponse()
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
                status_json = g['status']
                periods_json = g['periods'] 
                #print(json.dumps(team_json, indent=4))
                #print(json.dumps(score_json, indent=4))
                
                home_team = team_json['home']['name']
                away_team = team_json['visitors']['name']
                home_score = score_json['home']['points']
                away_score = score_json['visitors']['points']
                current_clock = status_json['clock']
                current_quarter = periods_json['current']

                #print(f'{home_team} ({home_score}) -- {away_team} ({away_score})')
                await ctx.send(f'```{home_team} ({home_score}) -- {away_team} ({away_score}) | Clock: {current_clock} Quarter: {current_quarter}```')
        else:
            await ctx.send('No live games right now!')

    @nba.command(
        name = "today", 
        description = "Get today's scores"
    )
    @checks.not_blacklisted()
    async def nba_today(self, ctx: Context):
        nba_conn = http.client.HTTPSConnection("v2.nba.api-sports.io")
        endpoint="games?league=standard&season=2022&date=" + str(date.today())
        nba_conn.request("GET", "/"+endpoint, headers=self.nba_headers)
        res = nba_conn.getresponse()
        data = res.read()

        response = json.loads(data.decode("utf-8"))
        #print(response)
        games = response["response"]
        if len(games) > 0:
            await ctx.send(f'{len(games)} games today.')
            for g in games:
                print(json.dumps(g, indent=4))
                team_json = g['teams']
                score_json = g['scores']
                status_json = g['status']
                periods_json = g['periods'] 
                #print(json.dumps(team_json, indent=4))
                #print(json.dumps(score_json, indent=4))
                
                home_team = team_json['home']['name']
                away_team = team_json['visitors']['name']
                home_score = score_json['home']['points']
                away_score = score_json['visitors']['points']
                current_clock = status_json['clock']
                current_quarter = periods_json['current']

                
                #print(f'{home_team} ({home_score}) -- {away_team} ({away_score})')
                await ctx.send(f'```{home_team} ({home_score}) -- {away_team} ({away_score}) | Clock: {current_clock} Quarter: {current_quarter}```')
        else:
            await ctx.send('No games today!')

    @nba.command(
        name = "stats", 
        description = "Get NBA player stats"
    )
    @checks.not_blacklisted()
    async def nba_stats(
        self, 
        ctx: Context,
        first_name: str,
        last_name: str,
        num_games: int = 1
    ):
        nba_conn = http.client.HTTPSConnection("v2.nba.api-sports.io")

        endpoint="players?name="+quote(last_name)
        nba_conn.request("GET", "/"+endpoint, headers=self.nba_headers)
        res = nba_conn.getresponse()
        data = res.read()

        response = json.loads(data.decode("utf-8"))
        print(response)
        exact_player_id = 0
        players = response["response"]
        if len(players) > 1:
            for p in players:
                if (p['firstname']).upper() == (first_name).upper():
                    exact_player_id = p['id']
        elif len(players) == 1:
            exact_player_id = players[0]['id']
        else:
            exact_player_id = 0
        print(exact_player_id)

        nba_conn.request("GET", "/players/statistics?season=2022&id="+str(exact_player_id), headers=self.nba_headers)
        res = nba_conn.getresponse()
        data = res.read()
        response = json.loads(data.decode("utf-8"))
        #print(json.dumps(response, indent=4))
        stats = response["response"]
        if len(stats) > 0:
            await ctx.send(f'Getting the past {num_games} game(s).')
            count = 1
            for s in stats:
                print(json.dumps(s, indent=4))
                count = count+1
                if count > int(num_games):
                    break    
        else:
            await ctx.send("No stats for "+first_name+" "+last_name+".")

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(NBA(bot))
