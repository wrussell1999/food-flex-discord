import discord
from discord.ext import commands
import random
from .data import *
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
        if channel_nick == "main":
            channel = bot.get_channel(config.config['food_chat_id'])
            await channel.send(output)
        elif channel_nick == "flex":
            channel = bot.get_channel(config.config['food_flex_channel_id'])
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
    if len(overall_score['score']) != 0:
        embed = discord.Embed(title="Winners", description="Highest score for term 2", colour=0xff0000)
        embed.set_footer(text="It's all to play for...")
        max_vote = max(overall_score['score'])
        value_str = "Score: " + str(max_vote)
        winner_indexes = [i for i, j in enumerate(overall_score['score']) if j == max_vote]
        if len(winner_indexes) > 1:
            winners = []
            for index, winner_index in enumerate(winner_indexes):
                winners.append(bot.get_guild(config.config['server_id']).get_member(overall_score['users'][winner_index]))
            for index, member in enumerate(winners):
                embed.add_field(name=member.nick, value=value_str)
            logger.debug("Command: Multiple winners")
        else:
            winner = bot.get_guild(config.config['server_id']).get_member(overall_score['users'][winner_indexes[0]])
            embed.add_field(name=winner.nick, value=value_str)
            logger.debug("Command: Single winner")

        await ctx.send(embed=embed)
        await ctx.message.delete()
    else:
        await ctx.send("There are currently no winners")
        await ctx.message.delete()


@data.command(description="Shows the current daily data as dict")
async def get_data(ctx):
    embed = discord.Embed(title="Daily Data", colour=0xff0000)
    embed.add_field(name="Submissions", value=daily_data['submissions'])
    embed.add_field(name="Voters", value=daily_data['voters'])
    embed.add_field(name="Votes", value=daily_data['votes'])
    await ctx.send(embed=embed)


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
        data_dict_to_json()
        await ctx.message.delete()


@data.command(description="Arguments: data, score")
async def force_json_dump(ctx, file: str):
    if await bot.is_owner(ctx.author):
        if file == "data":
            data_dict_to_json()
        elif file == "score":
            score_dict_to_json()
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
