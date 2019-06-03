import discord
from discord.ext import commands
import datetime
import random
from builtins import bot
from ..util.data import *
from ..util import config
from ..util.setup_period import *

logger = config.initilise_logging()
sorted_scoreboard_dict = {}

def update_score(winner, score):
    logger.debug("Score value: " + str(score))
    if winner.id in overall_score['users']:
        index = overall_score['users'].index(winner.id)
        overall_score['score'][index] += score
    else:
        overall_score['users'].append(winner.id)
        overall_score['score'].append(score)
    score_dict_to_json()

def update_leaderboard():
    channel = bot.get_channel(config.config['leaderboard_channel_id'])
    embed = discord.Embed(
        title="LEADERBOARD", description="Overall scores this term", colour=0xff0000)
    sorted_scoreboard_dict = sort_leaderboard()
    message = channel.fetch_message(config['leaderboard_messsage_id'])
    get_scores(sorted_scoreboard_dict['users'], sorted_scoreboard_dict['scores'], message)

def sort_leaderboard():
    sorted_scoreboard_dict['users'] = [x for _, x in sorted(
        zip(overall_score['score'], overall_score['users']), reverse=True)]
    sorted_scoreboard_dict['scores'] = [x for _, x in sorted(
        zip(overall_score['score'], overall_score['score']), reverse=True)]
    return sorted_scoreboard_dict

def get_scores(users, scores, message):
    embed = embed
    for index, val in enumerate(users):
        user = bot.get_guild(config.config['server_id']).get_member(val)
        score = "Score: " + str(scores[index])
        embed.add_field(name=user.nick, value=score, inline=False)
    await message.edit(embed=embed)
