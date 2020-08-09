import discord
import asyncio
import datetime
import builtins
import os
import sys
from dotenv import load_dotenv

import foodflex.util.logging as logging
logging.init()
from foodflex.util.logging import logger

builtins.__version__ = '3.0.0'
builtins.bot = commands.Bot(command_prefix="-ff ")

# all other module imports are after bot, so that they can access it
import foodflex.data.firestore as firestore
import foodflex.data.static as static
import foodflex.util.commands as commands
import foodflex.periods.voting as voting
import foodflex.periods.results as results
import foodflex.periods.messages as messages
import foodflex.periods.leaderboard as leaderboard
import foodflex.periods.submissions as submissions

def main():
    load_dotenv()
    sys.stdout.flush()
    logger.info(f'Starting Food Flex v{__version__}')
    static.load()
    logger.info(f'period=\'{data.period}\', mode=\'{data.mode}\' people={len(data.participants)}')
    bot.loop.create_task(check_time_periods())
    bot.run(config.token)

@bot.event
async def on_ready():
    global main_channel, leaderboard_channel, guild, admin_role
    logger.debug('Finding text channels...')
    builtins.main_channel = bot.get_channel(int(os.getenv('MAIN_CHANNEL_ID')))
    builtins.leaderboard_channel = bot.get_channel(int(os.getenv('LEADERBOARD_CHANNEL_ID')))
    builtins.guild = bot.get_guild(int(os.getenv('SERVER_ID')))
    builtins.admin_role = guild.get_role(int(os.getenv('ADMIN_ROLE_ID')))
    logger.info('Food Flex is online!')

@bot.event
async def on_message(message):
    # don't respond to our own messages
    await bot.process_commands(message)
    if message.author.bot:
        return
    # ignore messages in any channel but the main one
    if message.channel != main_channel:
        return

    if data.period == 'submissions' and len(message.attachments) > 0:
        logger.info(f'Submission from \'{message.author.display_name}\' ({str(message.author.id)})')
        await submissions.process_submission(message)

    elif data.period == 'voting' and len(message.clean_content) == 1:
        logger.info(f'Vote \'{message.clean_content}\' from \'{message.author.display_name}\' ({str(message.author.id)})')
        await voting.check_vote(message)

async def check_time_periods():
    await bot.wait_until_ready()

    # Repeat every 60 seconds
    while True:
        now = datetime.datetime.now()
        day = now.strftime('%a')
        hour = int(now.strftime('%H'))
        minute = int(now.strftime('%M'))

        # Submissions
        if day == 'Mon' and hour == 10 and minute == 00:
            data.change_period('submissions')
            await submissions.submission_period()

        # Submissions reminder
        elif day == 'Sat' and hour == 11 and minute == 00:
            await submissions.submission_reminder()

        # Voting
        elif day == 'Sat' and hour == 12 and minute == 00 and len(data.participants) > 1:
            data.change_period('voting')
            await voting.voting_period()

        # Vote reminder
        elif day == 'Sun' and hour == 11 and minute == 00 and len(data.participants) > 1:

            await voting.voting_reminder()
            await voting.individual_vote_reminder()

        # Results
        elif day == 'Sun' and hour == 22 and minute == 00 and len(data.participants) > 1:
            data.change_period('results')
            await results.results_period()

        await asyncio.sleep(60)
