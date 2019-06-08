import discord
from discord.ext import commands
import datetime
import random
import json
from builtins import bot
from ..util.data import leaderboard_data, save_leaderboard
from ..util.config import config, save_config, initilise_logging

logger = initilise_logging()


def update_score(winner, score):
    logger.debug("Score value: " + str(score))

    if winner.id not in leaderboard_data:
        leaderboard_data[str(winner.id)] = {
            'nick': winner.nick,
            'score': 1
        }
    else:
        leaderboard_data[str(winner.id)]['score'] += 1
    save_leaderboard()


async def update_leaderboard():
    channel = bot.get_channel(config['leaderboard_channel_id'])

    users = [(leaderboard_data[key]['nick'], leaderboard_data[key]['score'])
             for key in leaderboard_data]
    users.sort(key=lambda tuple: tuple[1], reverse=True)

    channel = bot.get_channel(config['leaderboard_channel_id'])
    if 'leaderboard_message_id' in config:
        message = await channel.fetch_message(
            config['leaderboard_message_id'])
        embed = get_embed(users)
        await message.edit(embed=embed)

    else:
        embed = get_embed(users)
        await channel.send(embed=embed)
        message_id = channel.last_message_id
        config['leaderboard_message_id'] = message_id
        save_config()


async def update_scores(users, scores, message):
    embed = get_embed(users, scores)
    await message.edit(embed=embed)


def get_embed(users):
    now = datetime.datetime.now()
    date_str = "Overall scores this term - " + \
        str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    embed = discord.Embed(
        title="Leaderboard", description=date_str, colour=0xff0000)

    for value in users:
        score = "Score: " + str(value[1])
        embed.add_field(name=value[0], value=score, inline=False)
    return embed


@bot.command()
async def refresh_scores(ctx):
    await ctx.message.delete()
    await update_leaderboard()
