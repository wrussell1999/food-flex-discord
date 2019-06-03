import discord
from discord.ext import commands
import datetime
import random
from builtins import bot
from ..util import config
from . import submissions
from . import voting

logger = config.initilise_logging()

@bot.event    
async def on_message(message):
    channel = bot.get_channel(config.config['food_flex_channel_id'])
    now = datetime.datetime.now()
    hour = int(now.strftime("%H"))
    minute = int(now.strftime("%M"))
    await bot.process_commands(message)

    if message.channel == channel:
        if len(message.attachments) > 0 and hour >= 12 and hour <= 23: # SUBMISSION
            logger.info("Submission from " + message.author.nick)
            await submissions.process_submission(message, channel)

        if len(message.attachments) == 0 and (hour >= 00 and hour < 12) and (len(str(message.clean_content)) == 1 or message.clean_content == ':b:'): # VOTING
            logger.info("Vote from: " + message.author.nick + ", Vote: " + str(message.clean_content))
            await voting.check_vote(message)
