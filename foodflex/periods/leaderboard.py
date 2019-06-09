import discord
from discord.ext import commands
import datetime
import random
import json
from builtins import bot

import foodflex.util.data as data
import foodflex.util.config as config

logger = config.initilise_logging()


def update_score(user_id, user_nick):
    # Checks if the user is already on the leaderboard
    print("user_id: " + user_id)
    print("user_nick: " + user_nick)
    if user_id not in data.leaderboard_data:
        # Adds user to leaderboard
        data.leaderboard_data[user_id] = {
            'nick': user_nick,
            'score': 1
        }
    else:
        data.leaderboard_data[user_id]['score'] += 1
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
    date_str = "Updated: " + \
        str(now.day) + "/" + str(now.month) + "/" + str(now.year)

    # Makes an embed
    embed = discord.Embed(
        title="Leaderboard",
        description="Overall scores this term",
        colour=0xff0000)
    embed.set_footer(text=date_str)
    # Adds the users to the embed
    for value in users:
        score = "Score: " + str(value[1])
        embed.add_field(name=value[0], value=score, inline=False)
    return embed
