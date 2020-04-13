import requests
import json
from discord.ext import commands

# BOT
TOKEN = str(open("TOKEN.txt").readline())
bot = commands.Bot(command_prefix="?")


@bot.event
async def on_ready():
    print("Ready!")


@bot.command(name="korona", help="Podaje statystyki koronawirusa w PL")
async def korona_stats(ctx, country='poland'):
    try:
        url = "https://covid-193.p.rapidapi.com/statistics"

        querystring = {"country": country}

        headers = {
            'x-rapidapi-host': "covid-193.p.rapidapi.com",
            'x-rapidapi-key': str(open("KEY.txt").readline())
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        message = response.json()
        json_response = message['response']
        zero = json_response[0]
        cases = zero['cases']
        deaths = zero['deaths']
        await ctx.send("**" + country.capitalize() + ":" + "**")
        await ctx.send('***Przypadki:***\n \
            Nowe przypadki: {}\n \
            Obecne przypadki: {}\n \
            Przypadki krytyczne: {}\n \
            Wyleczone przypadki: {}\n \
            Wszytskie potwierdzone przypadki: {}\n \
    ***Deduwy:***\n \
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
