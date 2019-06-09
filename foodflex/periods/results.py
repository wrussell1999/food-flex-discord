import discord
from discord.ext import commands
import datetime
import asyncio
import random
from builtins import bot
import foodflex.util.data as data
import foodflex.util.config as config
import foodflex.periods.leaderboard as leaderboard

logger = config.initilise_logging()
sorted_submissions_dict = {}


async def results_period(channel):
    logger.info("RESULTS")
    activity = discord.Activity(
        name="for shit food", type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.idle, activity=activity)

    users = []
    for key in data.daily_data:
        if data.daily_data[key]['submitted']:
            tuple = (data.daily_data[key]['nick'], data.daily_data[key]['votes'])
            users.append(tuple)
    users.sort(key=lambda tuple: tuple[1], reverse=True)

    winner_message = await get_winner(channel)

    embed = discord.Embed(title="Results", description="", colour=0xff0000)
    embed.set_author(name=winner_message)

    for user in users:
        votes = "Votes: " + str(user[1])
        embed.add_field(name=user[0], value=votes, inline=False)

    await channel.send(embed=embed)
    await leaderboard.update_leaderboard()

    # Reset the daily data
    data.daily_data.clear()
    data.save_data()


async def get_winner(channel):

    users = []
    for key in data.daily_data:
        if data.daily_data[key]['submitted'] and data.daily_data[key]['voted']:
            tuple = (data.daily_data[key]['nick'],
                     data.daily_data[key]['votes'])
            users.append(tuple)
    users.sort(key=lambda tuple: tuple[1], reverse=True)

    max_votes = users[0][1]
    if len(users) == 0 or max_votes == 0:
        embed = discord.Embed(
            title="No winner",
            description="The potential winners were disqualified",
            colour=0xff0000)
        await channel.send(embed=embed)
        return "No winner"

    winner_message = "Winners: "
    for user in users:
        if user[1] != max_votes:
            users.remove(user)
        else:
            winner_message += user[0] + ", "
    return winner_message
