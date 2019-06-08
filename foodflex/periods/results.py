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

    winner_message = await get_winner(channel, users)

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


async def get_winner(channel, users):
    for user_id in data.daily_data:
        if not data.daily_data[user_id]['voted']:
            await disqualify_winner(user_id, users, channel)

    if len(data.daily_data) == 0:  # won't work
        embed = discord.Embed(
            title="No winner",
            description="The potential winners were disqualified",
            colour=0xff0000)
        await channel.send(embed=embed)
        return "No winner"

    max_vote = users[0][1]
    winner_message = "Winner: "
    max_index = [index for index, vote in enumerate(
        data.daily_data['votes']) if vote == max_vote]

    if len(max_index) > 1:
        winner_message = "Winners: "

    for index, value in enumerate(data.daily_data['submissions']):
        if data.daily_data['votes'][index] == max_vote:
            winner = bot.get_guild(
                config['guild_id']).get_member(value)
            winner_message += winner.nick + ", "
            leaderboard.update_score(winner, 1)
    return winner_message


async def disqualify_winner(key, users, channel):
    user = bot.get_guild(
        config['guild_id']).get_member(key)

    winner_message = "Winner disqualified: " + str(user.nick)

    embed = discord.Embed(
        title=winner_message, description="Winner did not vote, therefore " +
        "their submission is invalid", colour=0xff0000)

    # Remove user from the daily data
    await channel.send(embed=embed)
    del data.daily_data[str(user.id)]
    await asyncio.sleep(1)


@bot.command(description="Results for a current day. Requires at least one voter")
async def results(ctx):
    if await bot.is_owner(ctx.author):
        await results_period(bot.get_channel(
            config['food_flex_channel_id']))
        logger.debug("Results started manually")
        await ctx.message.delete()
