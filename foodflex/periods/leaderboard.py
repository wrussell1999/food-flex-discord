import discord
from discord.ext import commands
import datetime
import random
from builtins import bot
from ..util.data import leaderboard_data, save_leaderboard
from ..util import config

logger = config.initilise_logging()
sorted_scoreboard_dict = {}


def update_score(winner, score):
    logger.debug("Score value: " + str(score))

    if winner.id in leaderboard_data['users']:
        index = leaderboard_data['users'].index(winner.id)
        leaderboard_data['score'][index] += score
    else:
        leaderboard_data['users'].append(winner.id)
        leaderboard_data['score'].append(score)
    save_leaderboard()


async def update_leaderboard():
    channel = bot.get_channel(config.config['leaderboard_channel_id'])
    sorted_scoreboard_dict = sort_leaderboard()
    try:
        message = await channel.fetch_message(
            config.config['leaderboard_message_id'])
        await update_scores(sorted_scoreboard_dict['users'],
                            sorted_scoreboard_dict['scores'], message)
    except:
        await create_leaderboard(sorted_scoreboard_dict['users'],
                                 sorted_scoreboard_dict['scores'])


def sort_leaderboard():  # FIX ME
    return


async def update_scores(users, scores, message):
    embed = get_embed(users, scores)
    await message.edit(embed=embed)


async def create_leaderboard(users, scores):
    embed = get_embed(users, scores)
    channel = bot.get_channel(config.config['leaderboard_channel_id'])
    await channel.send(embed=embed)

    # Get the ID of the last message
    message_id = channel.last_message_id()
    logger.debug(message_id)
    config.config['leaderboard_message_id'] = message_id


def get_embed(users, scores):
    now = datetime.datetime.now()
    date_str = "Overall scores this term - " + \
        str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    embed = discord.Embed(
        title="Leaderboard", description=date_str, colour=0xff0000)
    for index, val in enumerate(users):
        user = bot.get_guild(config.config['guild_id']).get_member(val)
        score = "Score: " + str(scores[index])
        embed.add_field(name=user.nick, value=score, inline=False)
    return embed


@bot.command()
async def refresh_scores(ctx):
    await update_leaderboard()
