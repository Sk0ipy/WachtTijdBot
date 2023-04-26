import asyncio
import datetime
import json

import discord
import requests
from discord.ext import commands

from config import *

# get the json data
data = json.load(open("data.json"))

"""
start with the start of the discord bot
"""

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())
bot.remove_command("help")

config = {
    "efteling": {
        "token_efteling": efteling_token,
        "channel_id_efteling": efteling_id
    },

}

"""
this will send every 5 minutes a message with the queue times of the desired park to the desired channel, the message will be deleted after 5 minutes and the bot will send a new message with the new queue times
"""


@bot.event
async def on_ready():
    channel = bot.get_channel(efteling_id)
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="Efteling Notifier",
                                  details="elke 5 minuten een update"))
    print("Efteling_bot is online!")
    # print the queue times every 5 minutes of all the rides per land in the park
    while True:

        # print last time update in a embed message
        embed = discord.Embed(title="Last update", color=0x00ff00)
        embed.set_footer(text="Efteling Notifier")
        embed.add_field(name="Last update", value=datetime.datetime.now().strftime("%H:%M:%S"), inline=False)
        await channel.send(embed=embed)

        url = f"https://queue-times.com/nl/parks/160/queue_times.json"
        response = requests.get(url)
        data = response.json()

        lands = data.get("lands")
        if not lands:
            return "lands not found"

        for land in lands:
            land_name = land["name"]
            rides = land["rides"]
            ride_per_land = [ride["name"] for ride in rides], [ride["wait_time"] for ride in rides]

            print(ride_per_land)
            # create embed message for every land with the rides and the queue times
            embed = discord.Embed(title=f"Queue times {land_name}", color=0x00ff00)
            embed.set_footer(text="Efteling Notifier")
            for ride in rides:
                ride["wait_time"] = str(ride["wait_time"]) + " minuten"
                embed.add_field(name=ride["name"], value=ride["wait_time"], inline=False)
            # send the embed message to the desired channel

            await channel.send(embed=embed)



        await asyncio.sleep(300)
        await channel.purge(limit=100)





bot.run(efteling_token)
