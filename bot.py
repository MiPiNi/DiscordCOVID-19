import requests
import discord
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
    await bot.change_presence(activity=discord.Game(name="?help"))


@bot.command(name="korona", help="Podaje statystyki koronawirusa w danym panstwie.\n Uzycie: ?korona <country>")
async def korona_stats(ctx, country='poland'):
    try:
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


@bot.command(name="world", help="Podaje statystyki koronawirusa na swiecie")
async def world_stats(ctx):
    url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/worldstat.php"

    headers = {
        'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
        'x-rapidapi-key': KEY
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()
    await ctx.send("**[World]**")
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


@bot.command(name="history",
             help="Wyswietla statystyki z ostatnich 7 dni w Polsce.")
async def korona_history(ctx,):
    today = datetime.datetime.today()
    week_ago = str(datetime.datetime(year=today.year, month=today.month, day=today.day - 7, hour=0))
    day_before = str(datetime.datetime(year=today.year, month=today.month, day=today.day, hour=0))
    url = "https://api.covid19api.com/country/poland" + "?from=" + week_ago + "&to=" + day_before

    response = requests.request("GET", url)

    message = response.json()
    i = 0

    await ctx.send("**[Poland]**")

    while i <= 6:
        data = message[i]
        active = data['Confirmed'] - (data['Recovered'] + data['Deaths'])
        await ctx.send('***' + str(data['Date'])[:10] + '***\n \
**Przypadki:**\n \
                        Aktywne przypadki: {}\n \
                        Wyleczone przypadki: {}\n \
                        Wszystkie potwierdzone przypadki: {}\n \
**Deduwy:**\n \
                        Deduwy: {}\n'.format(active,
                                           data['Recovered'],
                                           data['Confirmed'],
                                           data['Deaths']))
        i += 1


bot.run(TOKEN)
