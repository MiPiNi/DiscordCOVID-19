import requests
import json
import datetime
from discord.ext import commands

# BOT
TOKEN = str(open("TOKEN.txt").readline())
bot = commands.Bot(command_prefix="?")
KEY = str(open("KEY.txt").readline())


@bot.event
async def on_ready():
    print("Ready!")
    print(datetime.date.today())


@bot.command(name="korona", help="Podaje statystyki koronawirusa w PL")
async def korona_stats(ctx, country='poland'):
    try:
        if country == "world" or country == "World":
            url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/worldstat.php"

            headers = {
                'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
                'x-rapidapi-key': KEY
            }

            response = requests.request("GET", url, headers=headers)
            data = response.json()
            await ctx.send("**[" + country.capitalize() + "]**")
            await ctx.send('**Przypadki:**\n \
                Nowe przypadki: +{}\n \
                Obecne przypadki: {}\n \
                Wszystkie wyleczone przypadki: {}\n \
                Wszystkie potwierdzone przypadki: {}\n \
**Deduwy:**\n \
                Nowe deduwy: +{}\n \
                Laczne deduwy: {}'.format(data['new_cases'],
                                          data['active_cases'],
                                          data['total_recovered'],
                                          data['total_cases'],
                                          data['new_deaths'],
                                          data['total_deaths']))

        else:
            url = "https://covid-193.p.rapidapi.com/statistics"

            querystring = {"country": country}

            headers = {
                'x-rapidapi-host': "covid-193.p.rapidapi.com",
                'x-rapidapi-key': KEY
            }

            response = requests.request("GET", url, headers=headers, params=querystring)
            message = response.json()
            json_response = message['response']
            zero = json_response[0]
            cases = zero['cases']
            deaths = zero['deaths']
            await ctx.send("**[" + country.capitalize() + "]**")
            await ctx.send('**Przypadki:**\n \
                Nowe przypadki: {}\n \
                Obecne przypadki: {}\n \
                Przypadki krytyczne: {}\n \
                Wyleczone przypadki: {}\n \
                Wszystkie potwierdzone przypadki: {}\n \
**Deduwy:**\n \
                Nowe deduwy: {}\n \
                Laczne deduwy: {}'.format(cases['new'],
                                          cases['active'],
                                          cases['critical'],
                                          cases['recovered'],
                                          cases['total'],
                                          deaths['new'],
                                          deaths['total']))
    except IndexError:
        await ctx.send("Bledne panstwo!\nUzywaj angielskich nazw! (np. poland, usa, china)")


bot.run(TOKEN)
