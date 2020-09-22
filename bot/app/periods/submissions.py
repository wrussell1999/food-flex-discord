import discord
import random
import datetime
import foodflex.data.firestore as data
import foodflex.data.static as static
from foodflex.util.logging import logger

async def submission_period():
    logger.info('// Now in SUBMISSIONS period //')
    activity = discord.Activity(name=static.strings['submission_open_activity'],
                                type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    embed = discord.Embed(title=static.strings['submission_open_title'],
                          description=static.strings['submission_open'],
                          colour=0xff0000)
    await main_channel.send(embed=embed)

    logger.debug('Creating new weekly document')

    week_number = datetime.datetime.now().isocalendar()[1]
    data.create_new_weekly_document(document_name, week_number)

async def process_submission(message):
    user_id = str(message.author.id)
    logger.debug(f'Processing submission, msg id {user_id}')

    if user_id in data.weekly_data:
        logger.info('Submission invalid')

    else:
        try:
            url = message.attachments[0].proxy_url
        except IndexError:
            url = ''
            loggger.warn('Submission does not have an image attached')

        data.weekly_data[user_id] = {
            'nick': message.author.display_name,
            'submitted': True,
            'image_url': url,
            'voted': False,
            'votes': 0
        }

        await message.channel.send(random.choice(static.quotes['rude']))
        logger.info('Submission valid')
        data.update_weekly_document()

async def submission_reminder():
    embed = discord.Embed(title=static.strings['submission_reminder_title'],
                          description=static.strings['submission_reminder'],
                          colour=0xff0000)
    await main_channel.send(embed=embed)
