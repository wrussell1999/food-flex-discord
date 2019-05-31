import discord
from discord.ext import commands
import datetime
import random
from builtins import bot
from ..util.data import *
from ..util import config
from . import submissions
from . import voting

logger = config.initilise_logging()

@bot.event    
async def on_message(message):
    submission_channel = bot.get_channel(config.config['submission_channel_id'])
    voting_channel = bot.get_channel(int(config.config['voting_channel_id']))
    dev_channel = bot.get_channel(config.config['dev_channel_id'])
    now = datetime.datetime.now()
    hour = int(now.strftime("%H"))
    minute = int(now.strftime("%M"))
    second = int(now.strftime("%S"))
    await bot.process_commands(message)

    if len(message.attachments) > 0 and (hour >= 12 and hour <= 23) and (message.channel == submission_channel): # SUBMISSION
        logger.info("Submission from " + message.author.nick)
        await submissions.process_submission(message, submission_channel)

    if len(message.attachments) == 0 and (hour >= 00 and hour < 12) and message.channel == voting_channel and len(str(message.clean_content)) == 1: # VOTING
        logger.info("Vote from: " + message.author.nick + ", Vote: " + str(message.clean_content))
        await voting.check_vote(message, voting_channel)
