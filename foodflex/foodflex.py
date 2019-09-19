import discord
import asyncio
import datetime

import foodflex.util.logging as logging
logging.init()
logger = logging.logger

# All module are after bot, so that the other modules can access it
from foodflex.util.bot import bot
import foodflex.util.data as data
import foodflex.util.static as static
import foodflex.util.config as config
import foodflex.util.commands as commands
import foodflex.periods.voting as voting
import foodflex.periods.results as results
import foodflex.periods.messages as messages
import foodflex.periods.leaderboard as leaderboard
import foodflex.periods.submissions as submissions


def main():
    config.load()
    static.load()
    data.load_state()
    data.load_leaderboard()

    logger.info('Starting bot...')
    bot.loop.create_task(check_time_periods())
    bot.run(config.token)


@bot.event
async def on_ready():
    logger.info('Food Flex is online!')
    logger.info(f'period = \'{data.period}\', participants = {len(data.participants)}')


async def check_time_periods():
    await bot.wait_until_ready()
    channel = bot.get_channel(config.main_channel_id)

    # Repeat every 60 seconds
    while True:
        now = datetime.datetime.now()
        hour = int(now.strftime('%H'))
        minute = int(now.strftime('%M'))

        # Submissions
        if hour == 13 and minute == 00:
            data.period = 'submissions'
            await submissions.submission_period(channel)

        # Submissions reminder
        elif hour == 23 and minute == 00:
            await submissions.submission_reminder()

        # Voting
        elif (hour == 00 and minute == 00) and \
                len(data.participants) > 1:
            data.period = 'voting'
            await voting.voting_period(channel)

        # Vote reminder
        elif hour == 11 and minute == 00 and \
                len(data.participants) > 1:

            await voting.voting_reminder()
            await voting.individual_vote_reminder()

        # Results
        elif hour == 12 and minute == 00 and \
                len(data.participants) > 1:  # Needs
            data.period = 'results'
            await results.results_period(channel)

        await asyncio.sleep(60)
