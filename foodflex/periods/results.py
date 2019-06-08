import discord
from discord.ext import commands
import datetime
import asyncio
import random
from builtins import bot
from ..util.data import quotes, leaderboard_data, daily_data, strings, save_leaderboard, save_data
from ..util.config import config, initilise_logging
from .leaderboard import *

logger = initilise_logging()
sorted_submissions_dict = {}


async def results_period(channel):
    logger.info("RESULTS")
    activity = discord.Activity(
        name="for shit food", type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.idle, activity=activity)

    users = [(daily_data[key]['nick'], daily_data[key]['votes'])
             for key in daily_data if daily_data[key]['submitted'] is True]
    users.sort(key=lambda tuple: tuple[1], reverse=True)

    winner_message = await get_winner(channel, users)

    embed = discord.Embed(title="Results", description="", colour=0xff0000)
    embed.set_author(name=winner_message)

    for user in users:
        votes = "Votes: " + str(user[1])
        embed.add_field(name=user[0], value=votes, inline=False)

    await channel.send(embed=embed)
    await update_leaderboard()

    daily_data.clear()
    save_data()


async def get_winner(channel, users):
    [await disqualify_winner(key, users, channel)
     for key in daily_data if not daily_data[key]['voted']]

    no_winners = False
    [no_winners is True for key in daily_data
     if not daily_data[key]['voted'] and daily_data[key]['submitted']]

    if len(daily_data) == 0:  # won't work
        embed = discord.Embed(
            title="No winner",
            description="The potential winners were disqualified",
            colour=0xff0000)
        await channel.send(embed=embed)
        return "No winner"

    max_vote = users[0][1]
    winner_message = "Winner: "
    max_index = [index for index, vote in enumerate(
        daily_data['votes']) if vote == max_vote]

    if len(max_index) > 1:
        winner_message = "Winners: "

    for index, value in enumerate(daily_data['submissions']):
        if daily_data['votes'][index] == max_vote:
            winner = bot.get_guild(
                config['guild_id']).get_member(value)
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


async def disqualify_winner(key, users, channel):
    user = bot.get_guild(
        config['guild_id']).get_member(key)

    winner_message = "Winner disqualified: " + str(user.nick)

    embed = discord.Embed(
        title=winner_message, description="Winner did not vote, therefore " +
        "their submission is invalid", colour=0xff0000)

    await channel.send(embed=embed)
    del daily_data[str(user.id)]
    await asyncio.sleep(1)


@bot.command(description="Results for a current day. Requires at least one voter")
async def results(ctx):
    if await bot.is_owner(ctx.author):
        await results_period(bot.get_channel(
            config['food_flex_channel_id']))
        logger.debug("Results started manually")
        await ctx.message.delete()
