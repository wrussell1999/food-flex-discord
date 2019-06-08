import discord
from discord.ext import commands
import random
from .data import save_data, save_leaderboard, daily_data, leaderboard_data, quotes
from . import config
from builtins import bot


@bot.command(description="This explains how the food flex competition works - how to submit and vote")
async def helpme(ctx):
    embed = discord.Embed(title="Help", description="Use the different channels to submit and vote!", colour=0xff0000)
    embed.set_author(name="Food Flex - How this all works")
    embed.add_field(name="Submissions", value="Submit your photos of food here! One submission per user", inline=False)
    embed.add_field(name="Voting", value="Vote with the letter corresponding to your favourite flex. Only 1 vote per user. You can't vote for yourself", inline=False)
    embed.add_field(name="Results", value="See who won the most recent food flex!", inline=False)
    embed.add_field(name="Scoring", value="1 point for those with the highest number of votes")
    embed.set_footer(text="For more information, contact Will R")
    await ctx.send(embed=embed)
    await ctx.message.delete()


@bot.command(description="Arguments: channel_nick, output")
async def say(ctx, channel_nick: str, output: str):
    if await bot.is_owner(ctx.author):
        if channel_nick == "chat":
            channel = bot.get_channel(config.config['food_chat_id'])
            await channel.send(output)
        elif channel_nick == "flex":
            channel = bot.get_channel(config.config['food_flex_channel_id'])
            await channel.send(output)
        elif channel_nick == "leaderboard":
            channel = bot.get_channel(config.config['leaderboard_channel_id'])
            await channel.send(output)
        await ctx.message.delete()


@bot.group()
async def debug(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid debug command')


@debug.command(description="Just a test to see if the bot is responding. It posts a rude quote from Ramsay.")
async def test(ctx):
    await ctx.send(random.choice(quotes['rude']))
    await ctx.author.send("Test")
    await ctx.message.delete()


@debug.command()
async def ping(ctx):
    await ctx.send("pong")


@debug.command(description="Arguments: submission, voting, results")
async def force_status(ctx, period: str):
    if await bot.is_owner(ctx.author):
        activity = discord.Activity(name="for shit food",
                                    type=discord.ActivityType.watching)
        if period == "submissions":
            activity = discord.Activity(name="people submit shit food",
                                        type=discord.ActivityType.watching)
            await bot.change_presence(status=discord.Status.online,
                                      activity=activity)
        elif period == "voting":
            activity = discord.Activity(name="people vote on shit food",
                                        type=discord.ActivityType.watching)
            await bot.change_presence(status=discord.Status.online,
                                      activity=activity)
        elif period == "results":
            await bot.change_presence(status=discord.Status.idle,
                                      activity=activity)
    await ctx.message.delete()


@bot.group()
async def data(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid debug command')


@data.command(description="Winner of the Food Flex so far")
async def winner(ctx):
    await ctx.message.delete()


@data.command(description="Shows the current daily data as dict")
async def get_data(ctx):
    print(data)
    await ctx.send(str(data))


@data.command(description="Arguments: submissions, voters, votes")
async def clear(ctx, list: str):
    if await bot.is_owner(ctx.author):
        if list == "submissions":
            daily_data['submissions'].clear()
            logger.debug("Submissions cleared manually")
        elif list == "voters":
            daily_data['voters'].clear()
            logger.debug("Voters cleared manually")
        elif list == "votes":
            daily_data['votes'].clear()
            logger.debug("Votes cleared manually")
        save_data()
        await ctx.message.delete()


@data.command(description="Arguments: data, score")
async def force_json_dump(ctx, file: str):
    if await bot.is_owner(ctx.author):
        if file == "data":
            save_data()
        elif file == "score":
            save_leaderboard()
        await ctx.message.delete()


@data.command(description="All the rude Gordon Ramsay quotes")
async def rude_quotes(ctx):
    embed = discord.Embed(title="Rude Gordon Ramsay quotes",
                          description="All the quotes stored in ramsay_quotes.json",
                          colour=0xff0000)
    for index, val in enumerate(quotes['rude']):
        embed.add_field(name=str(index + 1), value=val, inline=False)
    await ctx.send(embed=embed)
    await ctx.message.delete()
