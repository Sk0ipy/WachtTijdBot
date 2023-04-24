import discord
from discord.ext import commands
from discord.ui import *

from config import *

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Bot is ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {synced} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")


@bot.tree.command(name="wachttijd", description="Get the waiting time for a country")
async def wachttijd(interaction: discord.Interaction, country: str):
    select = Select(
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
    view = View()
    view.add_item(select)
    await 


config = {
    'TOKEN': token,
    '!': prefix,
    'OWNER': owner,
    'NAME': name,
    'VERSION': version,
    'GUILD_ID': guild_id,

}

bot.run(config['TOKEN'])
