import discord
import random
import datetime
import app.data.firestore as data
import app.data.static as static
from app.util.logging import logger

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
    data.create_new_weekly_document(week_number)

async def process_submission(message):
    user_id = str(message.author.id)
    logger.debug(f'Processing submission, msg id {user_id}')
    if data.weekly_data != None and user_id in data.weekly_data:
        logger.info('Submission invalid')
        try:
            url = message.attachments[0].proxy_url
        except IndexError:
            url = ''
            loggger.warn('Submission does not have an image attached')


        data.weekly_data[user_id][u'image_url'] = url
        await message.channel.send(random.choice(static.quotes['rude']))
        logger.info('Submission overwritten')
    else:
        try:
            url = message.attachments[0].proxy_url
        except IndexError:
            url = ''
            loggger.warn('Submission does not have an image attached')

        data.weekly_data[user_id] = {
            u'nick': message.author.display_name,
            u'submitted': True,
            u'image_url': url,
            u'voted': False,
            u'votes': 0
        }
        await message.channel.send(random.choice(static.quotes['rude']))
        logger.info('Submission valid')
    data.update_weekly_document()

async def submission_reminder():
    embed = discord.Embed(title=static.strings['submission_reminder_title'],
                          description=static.strings['submission_reminder'],
                          colour=0xff0000)
    await main_channel.send(embed=embed)
