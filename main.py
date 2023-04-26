import discord
from discord.ext import commands
from discord.ui import *

from config import *
from parksPcountry import *

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
    embed.add_field(name="!gettimes", value="Laat alle wachttijden zien per pretpark", inline=False)

    await ctx.send(embed=embed)


@bot.command()
async def gettimes(ctx):
    select_country = Select(
        placeholder="kies uw land",
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
            placeholder="kies uw pretpark",
            options=[discord.SelectOption(label=park, value=park) for park in parks]
        )

        async def rides_or_land_callback(interaction):
            # check if the user selected a park or a land
            user_input = interaction.data["values"][0]
            rides_or_land = get_park_or_land(user_input, country)
            if rides_or_land == "land":
                # print all the lands in the park]
                lands = get_lands_per_park(user_input, country)
                select_land = Select(
                    placeholder="kies uw gebied",
                    options=[discord.SelectOption(label=land, value=land) for land in lands]
                )

                async def land_callback(interaction):
                    land = interaction.data["values"][0]
                    rides = get_rides_per_land(user_input, land, country)

                    # rides are 3 arrays, 1 for the name, 1 for the wait time and 1 for the status, but they are all in the same order i want them to be in the embed so i can just use 1 for loop
                    embed = discord.Embed(
                        title=f"{user_input} rides",
                        description="Hier zijn de attracties in dit gebied",
                        color=0x00ff00
                    )
                    for i in range(len(rides[0])):
                        embed.add_field(name=rides[0][i], value=f"Wachttijd: {rides[1][i]}\nStatus: {rides[2][i]}",
                                        inline=False)

                    await interaction.response.send_message(embed=embed)

                select_land.callback = land_callback
                view = View()
                view.add_item(select_land)
                await interaction.response.edit_message(content="Selecteer een land", view=view)


            elif rides_or_land == "park":
                rides = rides_per_park(user_input, country)

                # rides are 3 arrays, 1 for the name, 1 for the wait time and 1 for the status, but they are all in the same order i want them to be in the embed so i can just use 1 for loop
                embed = discord.Embed(
                    title=f"{user_input} rides",
                    description="Hier zijn de attracties in dit gebied",
                    color=0x00ff00
                )
                for i in range(len(rides[0])):
                    embed.add_field(name=rides[0][i], value=f"Wachttijd: {rides[1][i]}\nStatus: {rides[2][i]}",
                                    inline=False)

                await interaction.response.send_message(embed=embed)

            else:
                await interaction.response.send_message("Oeps, er is iets misgegaan")
                return

        select_park.callback = rides_or_land_callback
        view = View()
        view.add_item(select_park)
        await interaction.response.edit_message(content="Selecteer een pretpark", view=view)

        return

    # add other countries' logic here

    select_country.callback = country_callback
    view = View()
    view.add_item(select_country)
    await ctx.send("Selecteer een land", view=view)


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
