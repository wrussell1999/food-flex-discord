import discord
from discord.ext import commands
import datetime
import asyncio
import random
import builtins
from .util import config
from .util.data import *

bot = commands.Bot(command_prefix='flex:', owner_id=config.config['admin_id'])
builtins.bot = bot

from .periods.leaderboard import *
from .periods.results import *
from .periods.voting import *
from .periods.submissions import *
from .periods import messages
from .util import setup_period
from .util import flex_commands


def main():
    logger = config.initilise_logging()
    token = config.config['token']
    bot.loop.create_task(check_time_periods())
    bot.run(token)


@bot.event
async def on_ready():
    logger.info("Food Flex is online!")


async def check_time_periods():
    await bot.wait_until_ready()
    channel = bot.get_channel(config.config['food_flex_channel_id'])

    while True:
        now = datetime.datetime.now()
        hour = int(now.strftime("%H"))
        minute = int(now.strftime("%M"))

        if hour == 13 and minute == 00:
            await submission_period(channel)

        elif hour == 23 and minute == 00:
            logger.info("1 hour left for submissions")
            embed = discord.Embed(title="1 hour left for submissions",
                                  description="There's still time to submit today's flex!",
                                  colour=0xff0000)
            await channel.send(embed=embed)

        elif (hour == 00 and minute == 00) and \
                len(daily_data['submissions']) > 1:
            await voting_period(channel)

        elif hour == 11 and minute == 00 and \
                len(daily_data['submissions']) > 1:
            logger.info("1 hour left for voting")
            embed = discord.Embed(title="1 hour left for voting",
                                  description="There's still time to vote! Here are the current scores")
            embed = await get_embed(daily_data['submissions'],
                                    daily_data['votes'])
            embed.set_footer(
                text="Remember to vote for your submission to be valid!")
            await individual_vote_reminder()
            await channel.send(
                embed=embed)

        elif hour == 12 and minute == 00 and \
                len(daily_data) > 1:  # Needs 
            await results_period(channel)

        await asyncio.sleep(60)
