import discord
import logging
from discord.ext import commands
import datetime
from builtins import bot
from . import submissions
from . import voting
import foodflex.util.data as data
import foodflex.util.config as config

logger = logging.getLogger('food-flex')


@bot.event
async def on_message(message):
    flex_channel = bot.get_channel(config.config['food_flex_channel_id'])
    now = datetime.datetime.now()
    hour = int(now.strftime("%H"))
    minute = int(now.strftime("%M"))
    await bot.process_commands(message)

    if message.channel == flex_channel:
        if len(message.attachments) > 0 and \
                ((hour >= 12 and hour <= 23) or data.shared_prefs['submissions']):

            logger.info("Submission from '{}' ({})".format(message.author.nick, str(message.author.id)))
            await submissions.process_submission(message)

        if len(message.attachments) == 0 and \
                ((hour >= 00 and hour < 12) or data.shared_prefs['voting']) and len(message.clean_content) == 1:
            logger.info("Vote '{}' from '{}' ({})".format(message.clean_content, message.author.nick, str(message.author.id)))
            await voting.check_vote(message)
