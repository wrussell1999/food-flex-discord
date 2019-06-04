import discord
from discord.ext import commands
import datetime
import random
from builtins import bot
from ..util.data import *
from ..util import config
from ..util.setup_period import *

logger = config.initilise_logging()


async def voting_period(channel):
    logger.info("VOTING")
    activity = discord.Activity(name="people vote on shit food",
                                type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    embed = discord.Embed(title="VOTING!",
                          description="Vote for the best cooking of the day!",
                          colour=0xff0000)
    embed.set_footer(text="Respond in the chat with the appropriate letter")
    vote_value = 'A'
    for value in daily_data['submissions']:
        user = bot.get_guild(config.config['server_id']).get_member(value)
        embed.add_field(name=user.nick, value=str(vote_value), inline=False)
        vote_value = chr(ord(vote_value) + 1)    
    await channel.send(embed=embed)

    for value in daily_data['submissions']:
        daily_data['votes'].append(0)
    logger.info(str(daily_data['votes']))
    data_dict_to_json()


async def private_vote_reminder():
    for member_id in daily_data['submissions']:
        if member_id not in daily_data['voters']:
            user = bot.get_guild(config.config['server_id']).get_member(
                member_id)
            embed = discord.Embed(title="REMINDER!",
                                  description="Remember to vote for your submission to be valid!!!")
            embed.set_footer(text="You will be disqualified if you don't vote")
            await user.send(embed=embed)
            logger.debug("Vote reminder sent for " + str(user.nick))


async def check_vote(message):
    logger.info("Vote by: " + str(message.author.nick))
    if message.clean_content == ':b:':
        vote_index = 1
    else:
        vote_index = ord(message.clean_content[0].upper()) - 65
    logger.debug("vote_index: " + str(vote_index))  # this is an index
    if vote_index < len(daily_data['submissions']) and vote_index >= 0:  # Checks if it's in range
        duplicate = check_duplicate(vote_index, message)
        if duplicate is False:
            await is_valid(vote_index, message)
            await message.author.send(
                "Your vote has been submitted successfully")


def check_duplicate(vote_index, message):
    if check_self_vote(vote_index, message) is True or message.author.id in daily_data['voters']:
        return True
    else:
        return False


def check_self_vote(vote_index, message):
    if message.author.id in daily_data['submissions']:
        voter_index = daily_data['submissions'].index(message.author.id)
        if voter_index == vote_index:
            logger.warn("Invalid vote: same submission")
            return True
    else:
        return False


async def is_valid(vote_index, message):
    daily_data['voters'].append(message.author.id)
    daily_data['votes'][vote_index] += 1
    logger.debug("Vote List after: " + str(daily_data['votes']))
    data_dict_to_json()


@bot.command()
async def voting(ctx):
    if await bot.is_owner(ctx.author):
        await voting_period(bot.get_channel(
            config.config['food_flex_channel_id']))
        logger.debug("Voting started manually")
        await ctx.message.delete()
