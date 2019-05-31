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

def sort_scoreboard():
    sorted_scoreboard_dict['users'] = [x for _, x in sorted(zip(overall_score['score'], overall_score['users']), reverse=True)]
    sorted_scoreboard_dict['scores'] = [x for _, x in sorted(zip(overall_score['score'], overall_score['score']), reverse=True)]
    return sorted_scoreboard_dict

async def embed_scoreboard(users, scores, title, description):
    embed = discord.Embed(title=str(title), description=str(description), colour=0xff0000)
    for index, val in enumerate(users):
        user = bot.get_guild(config.config['server_id']).get_member(val)
        score = "Score: " + str(scores[index])
        embed.add_field(name=user.nick, value=score, inline=False)
    return embed

async def scoreboard(channel):
    sorted_scoreboard_dict = sort_scoreboard()
    embed = await embed_scoreboard(sorted_scoreboard_dict['users'], sorted_scoreboard_dict['scores'], "SCOREBOARD", "Scoreboard for this term")
    await channel.send(embed=embed)
    
@bot.command(description="Shows the overall score for the food flex")
async def score(ctx):
    await scoreboard(ctx.channel)
    await ctx.message.delete()
