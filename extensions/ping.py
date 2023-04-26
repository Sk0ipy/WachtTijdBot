import lightbulb, hikari

from config import *

config = {
    'TOKEN': main_token,
    '!': prefix,
    'OWNER': owner,
    'NAME': name,
    'VERSION': version,
    'GUILD_ID': guild_id,

}

bot = lightbulb.BotApp(token=config['TOKEN'], intents=hikari.Intents.ALL, default_enabled_guilds=[config['GUILD_ID']])

plugin = lightbulb.Plugin('ping')

def load(bot):
    bot.add_plugin(plugin)


@plugin.command()
@lightbulb.command('ping','ping command')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond('pong')



