import hikari
import lightbulb

from config import *

config = {
    'TOKEN': token,
    '!': prefix,
    'OWNER': owner,
    'NAME': name,
    'VERSION': version,
    'GUILD_ID': guild_id,

}

bot = lightbulb.BotApp(token=config['TOKEN'])


@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print("Bot is ready!")


@bot.command
@lightbulb.command('ping', 'shows the latency of the bot')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond(f'Pong! {round(bot.heartbeat_latency * 1000)}ms')

@bot.command
@lightbulb.option('number1', 'first number', type=int)
@lightbulb.option('number2', 'second number', type=int)
@lightbulb.command('add', 'adds two numbers')
@lightbulb.implements(lightbulb.SlashCommand)
async def add(ctx):
    await ctx.respond(
        f'{ctx.options["number1"]} + {ctx.options["number2"]} = {ctx.options["number1"] + ctx.options["number2"]}')



bot.run()
