import discord
from discord.ext import commands
import datetime
import asyncio
import random
import builtins
import foodflex.util.config as config
import foodflex.util.data as data

bot = commands.Bot(command_prefix='flex:', owner_id=config.config['admin_id'])
builtins.bot = bot
logger = config.initilise_logging()

# Imports are after bot, so that the other modules can access them
import foodflex.periods.leaderboard as leaderboard
import foodflex.periods.submissions as submissions
import foodflex.periods.voting as voting
import foodflex.periods.results as results
import foodflex.periods.messages as messages
import foodflex.util.commands as commands


def main():
    token = config.config['token']
    bot.loop.create_task(check_time_periods())
    bot.run(token)


@bot.event
async def on_ready():
    logger.info("Food Flex is online!")


async def check_time_periods():
    await bot.wait_until_ready()
    channel = bot.get_channel(config.config['food_flex_channel_id'])

    # Repeat every 60 seconds
    while True:
        now = datetime.datetime.now()
        hour = int(now.strftime("%H"))
        minute = int(now.strftime("%M"))

        # Submissions
        if hour == 13 and minute == 00:
            await submissions.submission_period(channel)

        # Submissions reminder
        elif hour == 23 and minute == 00:
            await submissions.submission_reminder()

        # Voting
        elif (hour == 00 and minute == 00) and \
                len(data.daily_data) > 1:
            await voting.voting_period(channel)

        # Vote reminder
        elif hour == 11 and minute == 00 and \
                len(data.daily_data) > 1:

            await voting.voting_reminder()
            await voting.individual_vote_reminder()

        # Results
        elif hour == 12 and minute == 00 and \
                len(data.daily_data) > 1:  # Needs
            await results.results_period(channel)

        await asyncio.sleep(60)
