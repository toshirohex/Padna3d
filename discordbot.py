import discord
from discord.ext import commands

client = discord.Client()
bot = commands.Bot(command_prefix='$')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


@bot.command()
async def hello(ctx):
    await ctx.send("Hello World")
    pass
client.run('NjY4MzE5NDk3NjYwMTM3NTAz.XiPjCQ.ZyqYGa2-5RY13fFObHCbo1Vi4kQ')
