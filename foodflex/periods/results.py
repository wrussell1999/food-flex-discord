import discord
from discord.ext import commands
import datetime
import asyncio
import random
from builtins import bot
from ..util.data import quotes, overall_score, daily_data, strings, score_dict_to_json, data_dict_to_json
from ..util.config import config, initilise_logging
from ..util.setup_period import *
from .leaderboard import *

logger = initilise_logging()
sorted_submissions_dict = {}


async def results_period(channel):
    logger.info("RESULTS")
    activity = discord.Activity(
        name="for shit food", type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.idle, activity=activity)

    winner_message = await get_winner(channel)

    embed = discord.Embed(title="RESULTS", description="", colour=0xff0000)
    embed.set_author(name=winner_message)

    users = [(daily_data[key]['nick'], daily_data[key]['votes'])
             for key in daily_data if daily_data[key]['submitted'] is True]
    users.sort(key=lambda tuple: tuple[1], reverse=True)

    for user in users:
        votes = "Votes: " + str(user[1])
        embed.add_field(name=user[0], value=votes, inline=False)

    await channel.send(embed=embed)
    await update_leaderboard()

    reset_daily_data()
    data_dict_to_json()


async def get_winner(channel):
    for index, value in enumerate(daily_data['submissions']):
        if not check_user_vote(value):
            await disqualify_winner(value, index, channel)

    if len(daily_data) == 0:  # won't work
        embed = discord.Embed(
            title="No winner",
            description="The potential winners were disqualified",
            colour=0xff0000)
        await channel.send(embed=embed)
        return "No winner"

    max_vote = max(daily_data['votes'])
    winner_message = "Winner: "
    max_index = [i for i, j in enumerate(
        daily_data['votes']) if j == max_vote]
    if len(max_index) > 1:
        winner_message = "Winners: "

    for index, value in enumerate(daily_data['submissions']):
        if daily_data['votes'][index] == max_vote:
            winner = bot.get_guild(
                config['server_id']).get_member(value)
            winner_message += winner.nick + ", "
            update_score(winner, 1)
    return winner_message


def check_user_vote(user):
    if user in daily_data['voters']:
        logger.debug("Winner voted - valid")
        return True
    else:
        logger.warning("Winner disqualified")
        return False


async def disqualify_winner(winner_id, index, channel):
    winner = bot.get_guild(
        config['server_id']).get_member(winner_id)
    winner_message = "Winner disqualified: " + str(winner.nick)
    embed = discord.Embed(
        title=winner_message, description="Winner did not vote, therefore " +
        "their submission is invalid", colour=0xff0000)
    await channel.send(embed=embed)
    del daily_data['votes'][index]
    del daily_data['submissions'][index]
    await asyncio.sleep(5)


@bot.command(description="Results for a current day. Requires at least one voter")
async def results(ctx):
    if await bot.is_owner(ctx.author) and len(daily_data['voters']) != 0:
        await results_period(bot.get_channel(
            config['food_flex_channel_id']))
        logger.debug("Results started manually")
        await ctx.message.delete()
