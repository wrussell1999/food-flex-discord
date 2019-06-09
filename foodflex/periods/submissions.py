import discord
from discord.ext import commands
import random
from builtins import bot
import foodflex.util.data as data
import foodflex.util.config as config

logger = config.initilise_logging()

async def submission_period(channel):
    logger.info('SUBMISSIONS')
    activity = discord.Activity(name=data.quotes['submission_open_activity'],
                                type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    embed = discord.Embed(title=data.quotes['submission_open_title'],
                          description=data.quotes['submission_open'],
                          colour=0xff0000)
    await channel.send(embed=embed)


async def process_submission(message, channel):
    user_id = str(message.author.id)
    if user_id in data.daily_data:
        logger.info('Submission invalid')
    else:
        new_letter = chr(ord('A') + len(data.daily_data))
        data.daily_data[user_id] = {
            'nick': message.author.nick,
            'submitted': True,
            'voted': False,
            'votes': 0
        }
        data.letter_to_user_id[new_letter] = user_id
        await channel.send(random.choice(data.quotes['rude']))
        data.save_data()
        logger.info('Submission valid, assigned letter \'{}\''.format(new_letter))

async def submission_reminder():
    channel = bot.get_channel(config.config['food_flex_channel_id'])
    embed = discord.Embed(title=data.strings['submission_reminder_title'],
                          description=data.strings['submission_reminder'],
                          colour=0xff0000)
    await channel.send(embed=embed)
