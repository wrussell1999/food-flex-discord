import discord
from discord.ext import commands
import datetime
import asyncio
import random
from builtins import bot
from data import *
import config
from setup_period import *
from scoreboard import *

logger = config.initilise_logging()
sorted_submissions_dict = {}

async def results_period(voting_channel, submission_channel, results_channel):
    logger.info("RESULTS")
    activity = discord.Activity(name="for shit food", type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    winner_message = await get_winner(results_channel)
    logger.debug(winner_message)
    embed = discord.Embed(title="RESULTS", description="", colour=0xff0000)
    embed.set_author(name=winner_message)
    embed.set_footer(text=random.choice(quotes['rude']))
    sorted_submissions_dict = sort_submissions()

    for index, val in enumerate(sorted_submissions_dict['votes']):
        votes_str = "Votes: "
        votes_str = votes_str + str(val)
        user_obj = bot.get_guild(config.config['server_id']).get_member(sorted_submissions_dict['submissions'][index])
        embed.add_field(name=user_obj.nick, value=votes_str, inline=False)
    await results_channel.send(embed=embed)
    reset_daily_data()
    data_dict_to_json()
    await channel_permissions(False, False, voting_channel, submission_channel)

async def get_winner(results_channel):
    for index, value in enumerate(daily_data['submissions']):
        if not check_winner_vote(value):
            disqualify_winner(value, index)

    if len(daily_data['submissions']) == 0:
        embed = discord.Embed(
            title="No winner", description="The potential winners were disqualified", colour=0xff0000)
        await results_channel.send(embed=embed)
        return "No winner"

    max_vote = max(daily_data['votes'])
    winner_message = "Winner: "
    winner_indexes = [i for i, j in enumerate(
        daily_data['votes']) if j == max_vote]

    if len(winner_indexes) > 1:
        winner_message = "Winners: "

    for index, value in enumerate(daily_data['submissions']):
        if daily_data['votes'][index] == max_vote:
            winner = bot.get_guild(
                config.config['server_id']).get_member(value)
            winner_message += winner.nick + ", "
            update_score(winner, 1)
    return winner_message

def check_winner_vote(winner):
    if winner.id in daily_data['voters']:
        logger.debug("Winner voted - valid")
        return True
    else:
        logger.warning("Winner disqualified")
        return False

async def disqualify_winner(winner, index):
    winner_message = "Winner disqualified: " + str(winner.nick)
    embed = discord.Embed(title=winner_message, description="Winner did not vote, therefore their submission is invalid", colour=0xff0000)
    await bot.get_channel(config.config['results_channel_id']).send(embed=embed)
    logger.debug("New winner selected" + str(daily_data['submissions'][index]))
    del daily_data['votes'][index]
    del daily_data['submissions'][index]
    await asyncio.sleep(5)

def sort_submissions():
    logger.debug("Sorting submissions into descending vote")
    sorted_submissions_dict['submissions'] = [x for _, x in sorted(zip(daily_data['votes'], daily_data['submissions']), reverse=True)]
    sorted_submissions_dict['votes'] = [x for _, x in sorted(zip(daily_data['votes'], daily_data['votes']), reverse=True)]
    return sorted_submissions_dict

@bot.command(description="Results for a current day. Requires at least one voter")
async def results(ctx):
    if await bot.is_owner(ctx.author) and len(daily_data['voters']) != 0:
        await results_period(bot.get_channel(config.config['voting_channel_id']), bot.get_channel(config.config['submission_channel_id']), bot.get_channel(config.config['results_channel_id']))
        logger.debug("Results started manually")
        await ctx.message.delete()
