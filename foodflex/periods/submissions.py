import random
import discord

import foodflex.util.data as data
import foodflex.util.config as config
import foodflex.util.static as static

from foodflex.util.logging import logger
from foodflex.util.bot import bot, __version__


async def submission_period(channel):
    logger.info('// Now in SUBMISSIONS period //')
    activity = discord.Activity(name=static.strings['submission_open_activity'],
                                type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    embed = discord.Embed(title=static.strings['submission_open_title'],
                          description=static.strings['submission_open'],
                          colour=0xff0000)
    await channel.send(embed=embed)

    logger.debug('Clearing participants & voting_map')
    data.participants.clear()
    data.voting_map.clear()
    data.save_state()


async def process_submission(message):
    user_id = str(message.author.id)
    logger.debug(f'Processing submission, msg id {user_id}')

    if user_id in data.participants:
        logger.info('Submission invalid')

    else:
        try:
            url = message.attachments[0].proxy_url
        except IndexError:
            url = ''
            loggger.warn('Submission does not have an image attached')

        data.participants[user_id] = {
            'nick': message.author.display_name,
            'submitted': True,
            'image_url': url,
            'voted': False,
            'votes': 0
        }

        await message.channel.send(random.choice(static.quotes['rude']))
        logger.info('Submission valid')
        data.save_state()

async def submission_reminder():
    channel = bot.get_channel(config.config['food_flex_channel_id'])
    embed = discord.Embed(title=static.strings['submission_reminder_title'],
                          description=static.strings['submission_reminder'],
                          colour=0xff0000)
    await channel.send(embed=embed)
