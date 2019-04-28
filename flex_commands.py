import discord
from discord.ext import commands
import random
from data import *
import config
#from main import scoreboard, submission_period, voting_period, results_period, reset_dict
from builtins import bot



@bot.command(pass_context=True, description="This explains how the food flex competition works - how to submit and vote")
async def helpme(ctx):
    embed = discord.Embed(title="Help", description="Use the different channels to submit and vote!", colour=0xff0000)
    embed.set_author(name="Food Flex - How this all works")
    embed.add_field(name="#submissions", value="Submit your photos of food here! One submission per user", inline=False)
    embed.add_field(name="#voting", value="Vote with the letter corresponding to your favourite flex. Only 1 vote per user. You can't vote for yourself", inline=False)
    embed.add_field(name="#results", value="See who won the most recent food flex!", inline=False)
    embed.add_field(name="Scoring", value="1 point for those with the highest number of votes")
    embed.set_footer(text="For more information, contact Will R")
    await ctx.send(embed=embed)
    await ctx.message.delete()

@bot.command(pass_context=True, description="Winner of the Food Flex so far")
async def winner(ctx):
    if (len(overall_score['score']) != 0):
        embed = discord.Embed(title="Winners", description="Highest score for term 2", colour=0xff0000)
        embed.set_footer(text="It's all to play for...")
        max_vote = max(overall_score['score'])
        value_str = "Score: " + str(max_vote)
        winner_indexes = [i for i, j in enumerate(overall_score['score']) if j == max_vote]
        if (len(winner_indexes) > 1):
            winners = []
            for index, winner_index in enumerate(winner_indexes):
                winners.append(bot.get_guild(config.config['server_id']).get_member(str(overall_score['users'][winner_index])))
            for index, member in enumerate(winners):
                embed.add_field(name=member.nick, value=value_str)
            logger.debug("Command: Multiple winners")
        else:
            winner = bot.get_guild(config.config['server_id']).get_member(str(overall_score['users'][winner_indexes[0]]))
            embed.add_field(name=winner.nick, value=value_str)
            logger.debug("Command: Single winner")
        logger.debug("Winner command")
        await ctx.send(embed=embed)
        await ctx.message.delete()
    else:
        await ctx.send("There are currently no winners")
        await ctx.message.delete()

@bot.command(pass_context=True, description="Just a test to see if the bot is responding. It posts a rude quote from Ramsay.")
async def test(ctx):
    await ctx.send(random.choice(quotes['rude']))
    await ctx.author.send("Test")
    await ctx.message.delete()

@bot.command(pass_context=True, description="All the rude Gordon Ramsay quotes")
async def rude_quotes(ctx):
    embed = discord.Embed(title="Rude Gordon Ramsay quotes", description="All the quotes stored in ramsay_quotes.json", colour=0xff0000)
    for index, val in enumerate(quotes['rude']):
        embed.add_field(name=str(index + 1), value=val, inline=False)
    await ctx.send(embed=embed)
    await ctx.message.delete()

@bot.command(pass_context=True)
async def say(ctx, channel: str, output: str):
    if (ctx.author.id == config.config['admin_id']):
        if (channel == "main"):
            food_chat = bot.get_channel(config.config['food_chat_id'])
            await food_chat.send(output)
        elif (channel == "submission"):
            submission_channel = bot.get_channel(config.config['submission_channel_id'])
            await submission_channel.send(output)
        elif (channel == "voting"):
            voting_channel = bot.get_channel(config.config['voting_channel_id'])
            await voting_channel.send(output)  
        elif (channel == "results"):
            results_channel = bot.get_channel(config.config['results_channel_id'])
            await results_channel.send(output)  
        await ctx.message.delete()

@bot.group(pass_context=True)
async def datag(ctx):
    if (ctx.invoked_subcommand is None):
        await bot.ctx('Invalid debug command')

@data.command(pass_context=True, description="Shows the current daily data as dict")
async def data(ctx):
    embed = discord.Embed(title="Daily Data", colour=0xff0000)
    embed.add_field(name="Submissions", value=daily_data['submissions'])
    embed.add_field(name="Voters", value=daily_data['voters'])
    embed.add_field(name="Votes", value=daily_data['votes'])
    await ctx.send(embed=embed)
    

@bot.group(pass_context=True)
async def debug(ctx):
    if (ctx.invoked_subcommand is None):
        await bot.ctx('Invalid debug command')

@data.command(pass_context=True)
async def clear(ctx, list: str):
    if (ctx.author.id == config.config['admin_id']):
        if (list == "submissions"):
            daily_data['submissions'].clear()
            logger.debug("Submissions cleared manually")
        elif(list == "voters"):
            daily_data['voters'].clear()
            logger.debug("Voters cleared manually")
        elif(list == "votes"):
            daily_data['votes'].clear()
            logger.debug("Votes cleared manually")
        data_dict_to_json()
        await ctx.message.delete()

@data.command(pass_context=True)
async def force_json_dump(ctx, file: str):
    if (ctx.author.id == config.config['admin_id']):
        if (file == "data"):
            data_dict_to_json()
        elif (file == "score"):
            score_dict_to_json()
        await ctx.message.delete()

@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send("pong")
    