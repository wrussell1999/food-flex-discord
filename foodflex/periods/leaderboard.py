import discord
from discord.ext import commands
import datetime
import random
import json
from builtins import bot

import foodflex.util.data as data
import foodflex.util.config as config

logger = config.initilise_logging()


def update_score(winner, score):
    logger.debug("Score value: " + str(score))

    if str(winner.id) not in data.leaderboard_data:
        data.leaderboard_data[str(winner.id)] = {
            'nick': winner.nick,
            'score': 1
        }
    else:
        data.leaderboard_data[str(winner.id)]['score'] += 1
    data.save_leaderboard()


async def update_leaderboard():
    channel = bot.get_channel(config.config['leaderboard_channel_id'])

    # Gets a list of users and scores (as tuple in descending order)
    users = [(data.leaderboard_data[key]['nick'], data.leaderboard_data[key]['score'])
             for key in data.leaderboard_data]
    users.sort(key=lambda tuple: tuple[1], reverse=True)

    channel = bot.get_channel(config.config['leaderboard_channel_id'])
    # Checks if the leaderboard has already been posted
    if 'leaderboard_message_id' in config.config:
        message = await channel.fetch_message(
            config.config['leaderboard_message_id'])
        embed = get_embed(users)
        await message.edit(embed=embed)
    else:
        # Creates new leaderboard
        embed = get_embed(users)
        await channel.send(embed=embed)
        message_id = channel.last_message_id
        config.config['leaderboard_message_id'] = message_id
        config.save_config()


def get_embed(users):
    # Gets the date
    now = datetime.datetime.now()
    date_str = "Overall scores this term - " + \
        str(now.day) + "/" + str(now.month) + "/" + str(now.year)

    # Makes an embed
    embed = discord.Embed(
        title="Leaderboard", description=date_str, colour=0xff0000)

    # Adds the users to the embed
    for value in users:
        score = "Score: " + str(value[1])
        embed.add_field(name=value[0], value=score, inline=False)
    return embed


@bot.command()
async def refresh_scores(ctx):
    await ctx.message.delete()
    await update_leaderboard()
