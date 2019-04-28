import discord
from discord.ext import commands
import datetime
import asyncio
import random
import builtins
import logging
import config
from data import *

bot = commands.Bot('flex:')
builtins.bot = bot

import flex_commands
import messages
from background import *

logger = config.initilise_logging()

@bot.event
async def on_ready(): 
    logger.info("Food Flex is online!")

async def my_background_task():
    await bot.wait_until_ready()
    submission_channel = bot.get_channel(config.config['submission_channel_id'])
    voting_channel = bot.get_channel(config.config['voting_channel_id'])
    results_channel = bot.get_channel(config.config['results_channel_id'])

    while not bot.is_closed:
        now = datetime.datetime.now()
        hour = int(now.strftime("%H"))
        minute = int(now.strftime("%M"))
        second = int(now.strftime("%S"))

        if (hour == 13 and minute == 00):
            await submission_period(submission_channel, voting_channel)
        elif (hour == 23 and minute == 00):
            logger.info("1 hour left for submissions")
            embed = discord.Embed(title="1 hour left for submissions", description="There's still time to submit today's flex!", colour=0xff0000)
            await submission_channel.send(embed=embed)
        elif ((hour == 00 and minute == 00) and len(daily_data['submissions']) > 1):
            await voting_period(submission_channel, voting_channel)
        elif (hour == 11 and minute == 00 and len(daily_data['submissions']) > 1):
            logger.info("1 hour left for voting")
            embed = await embed_scoreboard(daily_data['submissions'], daily_data['votes'], "1 hour left for voting", "There's still time to vote! Here are the current scores")
            embed.set_footer(text="Remember to vote for your submission to be valid!")
            await vote_reminder()      
            await voting_channel.send(embed=embed)
        elif ((hour == 12 and minute == 00) and len(daily_data['submissions']) > 1 and len(daily_data['voters']) > 0):
            await results_period(voting_channel, submission_channel, results_channel)
        await asyncio.sleep(60) # task runs every 60 seconds

token = config.config['token_id']
bot.loop.create_task(my_background_task())
bot.run(token)
