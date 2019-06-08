import discord
from discord.ext import commands
import datetime
import random
from builtins import bot
from ..util.data import daily_data, quotes
from ..util import config

logger = config.initilise_logging()


async def submission_period(channel):
    logger.info("SUBMISSIONS")
    activity = discord.Activity(name="people submit shit food",
                                type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    embed = discord.Embed(title="Submissions are open",
                          description="Submit a picture of your cooking!",
                          colour=0xff0000)
    await channel.send(embed=embed)


async def process_submission(message, channel):
    user_id_key = str(message.author.id)
    if str(message.author.id) in daily_data:
        logger.info("Submission invalid")
    else:
        user = bot.get_server(
            config.config['server_id']).get_member(message.author.id)
        daily_data[user_id_key] = {
            "nick": str(user.nick),
            "submitted": True,
            "voted": False,
            "votes": 0,
            "vote_letter": chr(ord('A') + len(daily_data))
        }
        await channel.send(random.choice(quotes['rude']))
        save_data()
        logger.info("Submission valid")


@bot.command()
async def submissions(ctx):
    if await bot.is_owner(ctx.author):
        await submission_period(bot.get_channel(
            config.config['food_flex_channel_id']))
        daily_data.clear()
        logger.info("Submissions started manually")
        await ctx.message.delete()


@bot.command()
async def close_submissions(ctx):
    if await bot.is_owner(ctx.author):
        activity = discord.Activity(name="bugs get fixed",
                                    type=discord.ActivityType.watching)
        await bot.change_presence(status=discord.Status.online,
                                  activity=activity)
        embed = discord.Embed(title="Submissions are closed",
                              description="We are currently working hard to " + 
                              "fix some problems! Check back later!",
                              colour=0xff0000)
        channel = bot.get_channel(config.config['food_flex_channel_id'])
        await channel.send(embed=embed)
