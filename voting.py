import discord
from discord.ext import commands
import datetime
import random
from builtins import bot
from data import *
import config
from setup_period import *

logger = config.initilise_logging()

async def voting_period(submission_channel, voting_channel):
    logger.info("VOTING")
    activity = discord.Activity(name="people vote on shit food", type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    embed = discord.Embed(title="VOTING!", description ="Vote for the best cooking of the day!", colour=0xff0000)
    embed.set_footer(text="Respond in the chat with the appropriate letter")
    vote_value = 'A'
    for value in daily_data[guild]['submissions']:
        user = bot.get_guild(int(guild)).get_member(value)
        embed.add_field(name=user.nick, value=str(vote_value), inline=False)
        vote_value = chr(ord(vote_value) + 1)    
    await voting_channel.send(embed=embed)

    for value in daily_data[guild]['submissions']:
        daily_data[guild]['votes'].append(0)
    logger.info(str(daily_data['votes']))
    data_dict_to_json()
    await channel_permissions(False, True, submission_channel, voting_channel, guild)

async def private_vote_reminder(guild):
    for member_id in daily_data[guild]['submissions']:
        if member_id not in daily_data[guild]['voters']:
            user = bot.get_guild(int(guild)).get_member(member_id)
            await user.send("Remember to vote for your submission to be valid!!!")
            logger.debug("Vote reminder sent for " + str(user.nick))

async def check_vote(message, voting_channel):
    guild = str(message.guild)
    logger.info("Vote by: " + str(message.author.nick))
    vote_index = ord(message.clean_content[0]) - 65
    logger.debug("vote_index: " + str(vote_index)) # this is an index
    # Checks if it's in range
    if vote_index < len(daily_data[guild]['submissions']) and vote_index >= 0:
        duplicate = check_duplicate(vote_index, voting_channel, message)
        if duplicate == False: 
            await is_valid(vote_index, voting_channel, message)

def check_duplicate(vote_index, voting_channel, message):
    guild = str(message.guild)
    if check_self_vote(vote_index, voting_channel, message) == True or message.author.id in daily_data[guild]['voters']:
        return True
    else:
        return False

def check_self_vote(vote_index, voting_channel, message):
    guild = str(message.guild)
    if message.author.id in daily_data[guild]['submissions']:
        voter_index = daily_data[guild]['submissions'].index(message.author.id)
        if voter_index == vote_index:
            logger.warn("Invalid vote: same submission")
            return True
    else:
        return False

async def is_valid(vote_index, voting_channel, message):
    guild = str(message.guild)
    daily_data[guild]['voters'].append(message.author.id)
    daily_data[guild]['votes'][vote_index] += 1
    logger.debug("Vote List after: " + str(daily_data[guild]['votes']))
    data_dict_to_json()

@bot.command()
async def voting(ctx):
    if await bot.is_owner(ctx.author):
        await voting_period(bot.get_channel(config.config['submission_channel_id']), bot.get_channel(config.config['voting_channel_id']))
        logger.debug("Voting started manually")
        await ctx.message.delete()
