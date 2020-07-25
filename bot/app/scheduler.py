import discord
import asyncio
import datetime

import foodflex.util.logging as logging
logging.init()

import foodflex.util.config as config
config.load()

# all other module imports are after bot, so that they can access it
import foodflex.util.bot
import foodflex.util.data as data
import foodflex.util.static as static
import foodflex.util.commands as commands
import foodflex.periods.voting as voting
import foodflex.periods.results as results
import foodflex.periods.messages as messages
import foodflex.periods.leaderboard as leaderboard
import foodflex.periods.submissions as submissions

from foodflex.util.logging import logger

def main():
    logger.info(f'Starting Food Flex v{__version__}')
    static.load()
    data.set_paths(config.data_root)
    data.load_state()
    data.load_leaderboard()

    print_state_info()

    logger.info('Starting bot...')
    bot.loop.create_task(check_time_periods())
    bot.run(config.token)


def print_state_info():
    logger.info(f'period=\'{data.period}\', mode=\'{data.mode}\' people={len(data.participants)}')


async def check_time_periods():
    await bot.wait_until_ready()

    # Repeat every 60 seconds
    while True:
        now = datetime.datetime.now()
        hour = int(now.strftime('%H'))
        minute = int(now.strftime('%M'))

            # Submissions
        if hour == 13 and minute == 00:
            data.change_period('submissions')
            await submissions.submission_period()

        # Submissions reminder
        elif hour == 23 and minute == 00:
            await submissions.submission_reminder()

        # Voting
        elif (hour == 00 and minute == 00) and \
                len(data.participants) > 1:
            data.change_period('voting')
            await voting.voting_period()

        # Vote reminder
        elif hour == 11 and minute == 00 and \
                len(data.participants) > 1:

            await voting.voting_reminder()
            await voting.individual_vote_reminder()

        # Results
        elif hour == 12 and minute == 00 and \
                len(data.participants) > 1:  # Needs
            data.change_period('results')
            await results.results_period()

        await asyncio.sleep(60)
