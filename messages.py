import discord
from discord.ext import commands
import datetime
import random
from data import *
import config
from builtins import bot

logger = config.initilise_logging()

@bot.event    
async def on_message(message):
    submission_channel = bot.get_channel(config.config['submission_channel_id'])
    voting_channel = bot.get_channel(int(config.config['voting_channel_id']))
    dev_channel = bot.get_channel(config.config['dev_channel_id'])
    now = datetime.datetime.now()
    hour = int(now.strftime("%H"))
    minute = int(now.strftime("%M"))
    second = int(now.strftime("%S"))
    await bot.process_commands(message)

    if len(message.attachments) > 0 and (hour >= 12 and hour <= 23) and (message.channel == submission_channel): # SUBMISSION
        logger.info("Submission from " + message.author.nick)
        await process_submission(message, submission_channel)

    if len(message.attachments) == 0 and (hour >= 00 and hour < 12) and message.channel == voting_channel and len(str(message.clean_content)) == 1: # VOTING
        logger.debug("Vote from: " + message.author.nick + ", Vote: " + message)
        await check_vote(message, voting_channel)

async def process_submission(message, submission_channel):
    duplicate = False
    for value in daily_data['submissions']:
        if (message.author.id == value):
            duplicate = True
    if duplicate == False:
        daily_data['submissions'].append(message.author.id)
        logger.info("Submission valid")
        await submission_channel.send(random.choice(quotes['rude']))
        data_dict_to_json()
    elif (duplicate == True):
        logger.info("Submission invalid")

async def check_vote(message, voting_channel):
    logger.info("Vote by: " + str(message.author.nick))
    raw = str(message.clean_content)
    vote = raw[0]
    vote_index = ord(vote) - 65
    logger.debug("vote_index: " + str(vote_index)) # this is an index
    if vote_index < len(daily_data['submissions']) and vote_index >= 0: # Checks if it's in range
        duplicate = validate_vote(vote_index, voting_channel, message)
        if (duplicate == True): 
            logger.info("Vote invalid")
        elif duplicate == False: 
            await valid_vote(vote_index, voting_channel, message)

def validate_vote(vote_index, voting_channel, message):
    if validate_self_vote(vote_index, voting_channel, message) == True:
        return True
    elif message.author.id in daily_data['voters']: 
        return True
    else:
        return False

def validate_self_vote(vote_index, voting_channel, message):
    if message.author.id in daily_data['submissions']:
        voter_index = daily_data['submissions'].index(message.author.id)
    else:
        voter_index = -1
    if voter_index == vote_index:
        logger.warn("Invalid vote: same submission")
        return True
    else:
        return False

async def valid_vote(vote_index, voting_channel, message):
    daily_data['voters'].append(message.author.id)
    daily_data['votes'][vote_index] += 1
    logger.debug("Vote List after: " + str(daily_data['votes']))
    data_dict_to_json()