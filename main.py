import discord
from discord.ext import commands
from discord.ui import *

from config import *
from parksPcountry import get_parks_per_country
from parksPcountry import rides_per_park
from parksPcountry import wait_time

"""
get all the parks per country with help of the json file
"""

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="WachtTijdBot | !help"))
    print("WachtTijdBot is online!")


"""
!help
"""


@bot.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(
        title="WachtTijdBot",
        description="WachtTijdBot is een bot die de wachttijden van de verschillende pretparken "
                    "laat zien",
        color=0x00ff00)
    embed.add_field(name="!help", value="Laat dit bericht zien", inline=False)
    embed.add_field(name="!getrides", value="Laat alle attracties zien van de gekozen pretpark", inline=False)
    embed.add_field(name="!gettimes", value="Laat alle wachttijden zien per pretpark", inline=False)

    await ctx.send(embed=embed)


"""
this is the !wtcountry, this will get the coutry that user want to see
"""


@bot.command()
async def getrides(ctx):
    select_country = Select(
        placeholder="Selecteer een land",
        options=[
            discord.SelectOption(label="Belgium", value="Belgium"),
            discord.SelectOption(label="Brazil", value="Brazil"),
            discord.SelectOption(label="Canada", value="Canada"),
            discord.SelectOption(label="China", value="China"),
            discord.SelectOption(label="Denmark", value="Denmark"),
            discord.SelectOption(label="England", value="England"),
            discord.SelectOption(label="France", value="France"),
            discord.SelectOption(label="Germany", value="Germany"),
            discord.SelectOption(label="Hong Kong", value="Honk Kong"),
            discord.SelectOption(label="Italy", value="Italy"),
            discord.SelectOption(label="Japan", value="Japan"),
            discord.SelectOption(label="Mexico", value="Mexico"),
            discord.SelectOption(label="Netherlands", value="Netherlands"),
            discord.SelectOption(label="Poland", value="Poland"),
            discord.SelectOption(label="South Korea", value="South Korea"),
            discord.SelectOption(label="Spain", value="Spain"),
            discord.SelectOption(label="Sweden", value="Sweden"),
            discord.SelectOption(label="United States", value="United States"),
        ]
    )

    async def country_callback(interaction):
        country = interaction.data["values"][0]
        parks = get_parks_per_country(country)
        select_park = Select(
            placeholder="Selecteer een pretpark",
            options=[discord.SelectOption(label=park, value=park) for park in parks]
        )

        async def park_callback(interaction):
            park = interaction.data["values"][0]
            park_rides = rides_per_park(park, country)

            embed = discord.Embed(
                title=f"{park} rides",
                description="Here are the rides in this park",
                color=0x00ff00
            )
            embed.add_field(name="Rides", value="\n".join(park_rides), inline=False)
            await interaction.response.send_message(embed=embed)

        select_park.callback = park_callback
        view = View()
        view.add_item(select_park)
        await interaction.response.edit_message(view=view)
        return

    # add other countries' logic here

    select_country.callback = country_callback
    view = View()
    view.add_item(select_country)
    await ctx.send("Select a country", view=view)


@bot.command()
async def gettimes(ctx):
    select_country = Select(
        placeholder="Selecteer een land",
        options=[
            discord.SelectOption(label="Belgium", value="Belgium"),
            discord.SelectOption(label="Brazil", value="Brazil"),
            discord.SelectOption(label="Canada", value="Canada"),
            discord.SelectOption(label="China", value="China"),
            discord.SelectOption(label="Denmark", value="Denmark"),
            discord.SelectOption(label="England", value="England"),
            discord.SelectOption(label="France", value="France"),
            discord.SelectOption(label="Germany", value="Germany"),
            discord.SelectOption(label="Hong Kong", value="Honk Kong"),
            discord.SelectOption(label="Italy", value="Italy"),
            discord.SelectOption(label="Japan", value="Japan"),
            discord.SelectOption(label="Mexico", value="Mexico"),
            discord.SelectOption(label="Netherlands", value="Netherlands"),
            discord.SelectOption(label="Poland", value="Poland"),
            discord.SelectOption(label="South Korea", value="South Korea"),
            discord.SelectOption(label="Spain", value="Spain"),
            discord.SelectOption(label="Sweden", value="Sweden"),
            discord.SelectOption(label="United States", value="United States"),
        ]
    )

    async def country_callback(interaction):
        country = interaction.data["values"][0]
        parks = get_parks_per_country(country)

        select_park = Select(
            placeholder="Selecteer een pretpark",
            options=[discord.SelectOption(label=park, value=park) for park in parks]
        )

        async def park_callback(interaction):
            park = interaction.data["values"][0]
            park_rides = wait_time(park, country)

            name = []
            time = []
            status = []
            for i in park_rides:
                name.append(i[0])
                time.append(i[1])
                status.append(i[2])

            embed = discord.Embed(
                title=f"{park} rides",
                description="Here are the rides in this park",
                color=0x00ff00
            )
            embed.add_field(name="Rides", value="\n".join(name), inline=True)
            embed.add_field(name="Time", value="\n".join(time), inline=True)
            embed.add_field(name="Status", value="\n".join(status), inline=True)
            await interaction.response.send_message(embed=embed)

        select_park.callback = park_callback
        view = View()
        view.add_item(select_park)
        await interaction.response.edit_message(view=view)
        return

    # add other countries' logic here

    select_country.callback = country_callback
    view = View()
    view.add_item(select_country)
    await ctx.send("Select a country", view=view)


"""
!clear, this will clear the whole chat
"""


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx):
    await ctx.channel.purge()
    # print("Berichten verwijderd") in red color in the server

    embed = discord.Embed(
        title="Berichten verwijderd",
        description="Alle berichten zijn verwijderd",
        color=0xFF0000)
    await ctx.send(embed=embed)


config = {
    'TOKEN': token,
    '!': prefix,
    'OWNER': owner,
    'NAME': name,
    'VERSION': version,
    'GUILD_ID': guild_id,

}

bot.run(config['TOKEN'])
