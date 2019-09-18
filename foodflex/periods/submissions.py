import discord
import logging
from discord.ext import commands
import random
from builtins import bot
import foodflex.util.data as data
import foodflex.util.config as config

logger = logging.getLogger('food-flex')


async def submission_period(channel):
    logger.info("// Now in SUBMISSIONS period //")
    activity = discord.Activity(name=data.strings['submission_open_activity'],
                                type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    embed = discord.Embed(title=data.strings['submission_open_title'],
                          description=data.strings['submission_open'],
                          colour=0xff0000)
    await channel.send(embed=embed)


async def process_submission(message):
    user_id = str(message.author.id)
    logger.debug(f'Processing submission, msg id {user_id}')

    if user_id in data.daily_data:
        logger.info('Submission invalid')

    else:
        try:
            url = message.attachments[0].proxy_url
        except IndexError:
            url = ''
            loggger.warn('Submission does not have an image attached')

        data.daily_data[user_id] = {
            'nick': message.author.display_name,
            'submitted': True,
            'image_url': url,
            'voted': False,
            'votes': 0
        }

        await message.channel.send(random.choice(data.quotes['rude']))
        logger.info('Submission valid')
        data.save_data()

async def submission_reminder():
    channel = bot.get_channel(config.config['food_flex_channel_id'])
    embed = discord.Embed(title=data.strings['submission_reminder_title'],
                          description=data.strings['submission_reminder'],
                          colour=0xff0000)
    await channel.send(embed=embed)
