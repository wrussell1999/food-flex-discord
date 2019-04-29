import discord
from discord.ext import commands
import datetime
import random
from builtins import bot
from data import *
import config
from setup_period import *

logger = config.initilise_logging()
sorted_scoreboard_dict = {}

def update_score(winner, score):
    logger.info("Scoreboard updated")
    logger.debug("Score value: " + str(score))
    if winner.id in overall_score['users']:
        index = overall_score['users'].index(winner.id)
        overall_score['score'][index] += score
    else:
        overall_score['users'].append(winner.id)
        overall_score['score'].append(score)
    score_dict_to_json()

def sort_scoreboard():
    logger.debug("Sorting scoreboard into descending score")
    sorted_scoreboard_dict['users'] = [x for _, x in sorted(zip(overall_score['score'], overall_score['users']), reverse=True)]
    sorted_scoreboard_dict['scores'] = [x for _, x in sorted(zip(overall_score['score'], overall_score['score']), reverse=True)]
    return sorted_scoreboard_dict

async def embed_scoreboard(users, scores, title, description):
    logger.debug("Scoreboard displayed")
    embed = discord.Embed(title=str(title), description=str(description), colour=0xff0000)
    for index, val in enumerate(users):
        user = bot.get_guild(config.config['server_id']).get_member(str(val))
        score = "Score: " + str(scores[index])
        embed.add_field(name=user.nick, value=score)
    return embed

async def scoreboard(channel):
    sorted_scoreboard_dict = sort_scoreboard()
    embed = await embed_scoreboard(sorted_scoreboard_dict['users'], sorted_scoreboard_dict['scores'], "SCOREBOARD", "Scoreboard for this term")
    await channel.send(embed=embed)

async def auto_scoreboard():
    sorted_scoreboard_dict = sort_scoreboard()
    embed = await embed_scoreboard(sorted_scoreboard_dict['users'], sorted_scoreboard_dict['scores'], "SCOREBOARD", "Scoreboard for this term")
    await bot.get_channel(config.config['results_channel_id']).send(embed=embed)

    
@bot.command(description="Shows the overall score for the food flex")
async def score(ctx):
    await scoreboard(ctx.channel)
    await ctx.message.delete()
