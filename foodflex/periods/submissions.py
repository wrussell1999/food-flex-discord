import discord
from discord.ext import commands
import datetime
import random
from builtins import bot
from ..util.data import *
from ..util import config
from ..util.setup_period import *

logger = config.initilise_logging()
async def submission_period(submission_channel, voting_channel):
    logger.info("SUBMISSIONS")
    activity = discord.Activity(name="people submit shit food", type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    embed = discord.Embed(title="Submissions are open", description="Submit a picture of your cooking!", colour=0xff0000)
    await submission_channel.send(embed=embed)
    await channel_permissions(True, False, submission_channel, voting_channel)

async def process_submission(message, submission_channel):
    duplicate = False
    for value in daily_data['submissions']:
        if (message.author.id == value):
            duplicate = True
    if duplicate == False:
        daily_data['submissions'].append(message.author.id)
        logger.info("Submission valid")
        await submission_channel.send(random.choice(quotes['rude']))
        data_dict_to_json()
    elif (duplicate == True):
        logger.info("Submission invalid")

@bot.command()
async def submissions(ctx):
    if await bot.is_owner(ctx.author):
        await submission_period(bot.get_channel(config.config['submission_channel_id']), bot.get_channel(config.config['voting_channel_id']))
        reset_daily_data()
        logger.info("Submissions started manually")
        await ctx.message.delete()

@bot.command()
async def close_submissions(ctx):
    if await bot.is_owner(ctx.author):
        activity = discord.Activity(name="people submit shit food", type=discord.ActivityType.watching)
        await bot.change_presence(status=discord.Status.online, activity=activity)
        embed = discord.Embed(title="Submissions are closed", description="We are currently working hard to fix some problems! Check back later!", colour=0xff0000)
        await submission_channel.send(embed=embed)
        await channel_permissions(False, False, bot.get_channel(config.config['submission_channel_id']), bot.get_channel(config.config['voting_channel_id']))

