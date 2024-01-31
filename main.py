import discord
import time
from datetime import datetime, date, time, timedelta
from discord.ext.commands import Bot
from discord.ext.commands import has_permissions
from discord.ext import commands

message_cooldown = commands.CooldownMapping.from_cooldown(5,15, commands.BucketType.user)
too_many_violeations = commands.CooldownMapping.from_cooldown(4,60, commands.BucketType.user)

intents = discord.Intents.all()
client = Bot(command_prefix='!', intents=intents)
@client.event
async def on_ready():
    i = 0
    for guild in client.guilds:
        i = i+1
    
    print("bot is in " + str(i) + " servers")


@client.event
async def on_message(message):
    await client.process_commands(message)
    if type(message.channel) is not discord.TextChannel or message.author.bot: return
    bucket = message_cooldown.get_bucket(message)
    retry_after = bucket.update_rate_limit()
    if retry_after:
        await message.delete()
        print("spam detected by " + message.author.name + " in " + message.guild.name)
        await message.channel.send("spam detected by " + message.author.mention , delete_after=10)
        violations = too_many_violeations.get_bucket(message)
        check = violations.update_rate_limit()
        if check:
            try:
                await message.author.timeout(timedelta(minutes = 10),reason = "spamming")
                print("gave " + message.author.name + " a timeout for 10 minutes in " + message.guild.name)
                await message.channel.send(message.author.mention + "has been muted for spamming")
            except:
                print("resumed to purging in " + message.guild.name)
                await message.channel.purge()
                await message.channel.send("deleted all messages in this channel",delete_after=10)
                

            

@client.command()
@has_permissions(manage_messages=True)
async def clearmess(ctx):
    print(ctx.message.author.name + " ran the !clearmess command in server " + ctx.guild.name + " , channel : " + ctx.channel.name)
    await ctx.channel.send("Clearing all mesages...")
    await ctx.channel.purge()

@clearmess.error
async def error(error, ctx):
    ctx.channel.send("command failed , error : " + error)

@client.command()
@has_permissions(manage_messages=True)
async def clearall(ctx):
    print(ctx.message.author.name + " ran the !clearall command in server " + ctx.guild.name + " , channel : " + ctx.channel.name)
    await ctx.channel.send("Clearing all mesages in all channels (might take a long time) ...")
    for channel in ctx.guild.channels:
        try:
            await channel.purge()
        except:
            pass

@clearall.error
async def error(error, ctx):
    ctx.channel.send("command failed , error : " + error)

@client.command()
@has_permissions(manage_channels=True)
async def clearchans(ctx):
    print(ctx.message.author.name + " ran the !clearchans command in server " + ctx.guild.name + " , channel : " + ctx.channel.name)
    await ctx.channel.send("Deleting all channels")
    for channel in ctx.guild.channels:
        await channel.delete()

@clearchans.error
async def error(error, ctx):
    ctx.channel.send("command failed , error : " + error)

with open("RepelerPro\\token.txt","r") as f:
    client.run(f.read())
