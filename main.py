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


logger = config.initilise_logging()
sorted_scoreboard_dict = {}
sorted_submissions_dict = {}
    
token = config.config['token_id']

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

async def submission_period(submission_channel, voting_channel):
    logger.info("SUBMISSIONS")
    embed = discord.Embed(title="Submissions are open", description="Submit a picture of your cooking!", colour=0xff0000)
    await submission_channel.send(embed=embed)
    await channel_permissions(True, False, submission_channel, voting_channel)

async def voting_period(submission_channel, voting_channel):
    logger.info("VOTING")
    embed = discord.Embed(title="VOTING!", description ="Vote for the best cooking of the day!", colour=0xff0000)
    embed.set_footer(text="Respond in the chat with the appropriate letter")
    vote_value = 'A'
    for value in daily_data['submissions']:
        user = bot.get_guild(config.config['server_id']).get_member(str(value))
        embed.add_field(name=user.nick, value=str(vote_value), inline=True)
        vote_value = chr(ord(vote_value) + 1)    
    await voting_channel.send(embed=embed)

    for value in daily_data['submissions']:
        daily_data['votes'].append(0)
    logger.info(str(daily_data['votes']))
    data_dict_to_json()
    await channel_permissions(False, True, submission_channel, voting_channel)

async def vote_reminder():
    logger.debug("Reminding users who submitted")
    for member_id in daily_data['submissions']:
        if member_id in daily_data['voters']:
            logger.debug(member_id + " has voted - no reminder")
        else:
            user = bot.get_guild(config.config['server_id']).get_member(member_id)
            await user.send("Remember to vote for your submission to be valid!!!")
            logger.debug("Vote reminder sent for " + str(user.nick))

async def results_period(voting_channel, submission_channel, results_channel):
    logger.info("RESULTS")
    winner_message = await get_winner(results_channel)
    embed = discord.Embed(title="RESULTS", description="", colour=0xff0000)
    embed.set_author(name=winner_message)
    embed.set_footer(text=random.choice(quotes['rude']))
    sorted_submissions_dict = sort_submissions()

    for index, val in enumerate(sorted_submissions_dict['votes']):
        votes_str = "Votes: "
        votes_str = votes_str + str(val)
        user_obj = bot.get_guild(config.config['server_id']).get_member(sorted_submissions_dict['submissions'][index])
        embed.add_field(name=user_obj.nick, value=votes_str, inline=True)
    await results_channel.send(embed=embed)
    reset_dict()
    data_dict_to_json()
    await channel_permissions(False, False, voting_channel, submission_channel)

def reset_dict():
    daily_data['submissions'].clear()
    daily_data['votes'].clear()
    daily_data['voters'].clear()
    logger.debug("daily_data reset")

async def get_winner(results_channel):
    logger.debug("Getting Winner")
    max_vote = max(daily_data['votes'])
    if (max_vote > 0):
        winner_indexes = [i for i, j in enumerate(daily_data['votes']) if j == max_vote]
        logger.debug("index of winners: "  + str(winner_indexes))
        winner_message = ""
        sorted_submissions_dict = sort_submissions()
        winner_true = False

        while (winner_true == False):
            if (len(winner_indexes) > 1 and len(daily_data['submissions']) > 1):
                logger.debug("Multiple winners")
                winners = []
                winner_message = "Winners: "

                for index, winner_index in enumerate(winner_indexes):
                    winners.append(bot.get_guild(config.config['server_id']).get_member(str(daily_data['submissions'][winner_index])))

                for index, member in enumerate(winners):
                    if (check_winner_vote(member) == True):
                        logger.debug("Selected Winner: " + member.nick)
                        update_score(member, 1)
                        winner_message += str(member.nick) + ", "
                        logger.info(winner_message)
                        winner_true = True
                    else:
                        await disqualify_winner(member, index)
            else:
                logger.debug("1 winner")
                winner = bot.get_guild(config.config['server_id']).get_member(str(daily_data['submissions'][winner_indexes[0]]))
                if (check_winner_vote(winner) == True):
                    update_score(winner, 1)
                    winner_message = "Winner: " + winner.nick
                    logger.info("Winner: " + str(winner.nick))
                    winner_true = True
                else:
                    await disqualify_winner(winner, winner_indexes[0])
    else:
        embed = discord.Embed(title="No winner", description="The potential winners were disqualified", colour=0xff0000)
        await results_channel.send(embed=embed)
        winner_message = "No winner"
    return winner_message

def check_winner_vote(winner):
    if winner.id in daily_data['voters']:
        logger.debug("Winner voted - valid")
        return True
    else:
        logger.warning("Winner disqualified")
        return False

async def disqualify_winner(winner, index):
    winner_message = "Winner disqualified: " + str(winner.nick)
    embed = discord.Embed(title=winner_message, description="Winner did not vote, therefore their submission is invalid", colour=0xff0000)
    await bot.get_channel(config.config['results_channel_id']).send(embed=embed)
    logger.debug("New winner selected" + str(daily_data['submissions'][index]))
    del daily_data['votes'][index]
    del daily_data['submissions'][index]


def update_score(winner, score):
    logger.info("Scoreboard updated")
    logger.debug("Score value: " + str(score))
    if winner.id in overall_score['users']:
        index = overall_score['users'].index(winner.id)
        overall_score['score'][index] += score
    else:
        overall_score['users'].append(winner.id)
        overall_score['score'].append(score)
    score_dict_to_json()

def sort_submissions():
    logger.debug("Sorting submissions into descending vote")
    sorted_submissions_dict['submissions'] = [x for _, x in sorted(zip(daily_data['votes'], daily_data['submissions']), reverse=True)]
    sorted_submissions_dict['votes'] = [x for _, x in sorted(zip(daily_data['votes'], daily_data['votes']), reverse=True)]
    return sorted_submissions_dict

def sort_scoreboard():
    logger.debug("Sorting scoreboard into descending score")
    sorted_scoreboard_dict['users'] = [x for _, x in sorted(zip(overall_score['score'], overall_score['users']), reverse=True)]
    sorted_scoreboard_dict['scores'] = [x for _, x in sorted(zip(overall_score['score'], overall_score['score']), reverse=True)]
    return sorted_scoreboard_dict

async def embed_scoreboard(users, scores, title, description):
    logger.debug("Scoreboard displayed")
    embed = discord.Embed(title=str(title), description=str(description), colour=0xff0000)
    for index, val in enumerate(users):
        user = bot.get_guild(config.config['server_id']).get_member(str(val))
        score = "Score: " + str(scores[index])
        embed.add_field(name=user.nick, value=score)
    return embed

async def scoreboard(channel):
    sorted_scoreboard_dict = sort_scoreboard()
    embed = await embed_scoreboard(sorted_scoreboard_dict['users'], sorted_scoreboard_dict['scores'], "SCOREBOARD", "Scoreboard for this term")
    await channel.send(embed=embed)

async def auto_scoreboard():
    sorted_scoreboard_dict = sort_scoreboard()
    embed = await embed_scoreboard(sorted_scoreboard_dict['users'], sorted_scoreboard_dict['scores'], "SCOREBOARD", "Scoreboard for this term")
    await bot.get_channel(config.config['results_channel_id']).send(embed=embed)

async def channel_permissions(before, after, channel_before, channel_after):
    guild = bot.get_guild(config.config['server_id'])
    await channel_before.set_permissions(guild.default_role, send_messages=before)
    await channel_after.set_permissions(guild.default_role, send_messages=after)
    logger.debug("Permissions updated")
    
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

    if ((len(message.attachments) > 0) and (hour >= 12 and hour <= 23) and (message.channel == submission_channel)): # SUBMISSION
        logger.debug("SUBMISSION MESSAGE: " + str(hour) + ":" + str(minute))
        logger.info("Submission from " + message.author.nick)
        await process_submission(message, submission_channel)

    if (len(message.attachments) == 0 and (hour >= 00 and hour < 12) and message.channel == voting_channel and len(str(message.clean_content)) == 1): # VOTING
        logger.debug("VOTING MESSAGE: " + str(hour) + ":" + str(minute))
        await check_vote(message, voting_channel)

async def process_submission(message, submission_channel):
    duplicate = False
    for value in daily_data['submissions']:
        if (message.author.id == value):
            duplicate = True
    if (duplicate == False):
        daily_data['submissions'].append(message.author.id)
        logger.debug("Submission valid")
        await submission_channel.send(random.choice(quotes['rude']))
        data_dict_to_json()
    elif (duplicate == True):
        logger.warning("User already submitted - submission invalid")

async def check_vote(message, voting_channel):
    logger.info("Vote by: " + str(message.author.nick))
    raw = str(message.clean_content)
    vote = raw[0]
    vote_index = ord(vote) - 65
    logger.debug("vote_index: " + str(vote_index)) # this is an index
    if (vote_index < len(daily_data['submissions']) and vote_index >= 0): # Checks if it's in range
        duplicate = validate_vote(vote_index, voting_channel, message)
        if (duplicate == True): 
            logger.warn("User already voted: invalid")
        elif(duplicate == False): 
            await valid_vote(vote_index, voting_channel, message)

def validate_vote(vote_index, voting_channel, message):
    if (validate_self_vote(vote_index, voting_channel, message) == True):
        return True
    elif message.author.id in daily_data['voters']: 
        return True
    else:
        return False

def validate_self_vote(vote_index, voting_channel, message):
    if (message.author.id in daily_data['submissions']):
        voter_index = daily_data['submissions'].index(message.author.id)
        logger.debug("voter_index: " + str(voter_index))
    else:
        voter_index = -1
    if (voter_index == vote_index):
        logger.warn("Invalid vote: same submission")
        return True
    else:
        return False

async def valid_vote(vote_index, voting_channel, message):
    daily_data['voters'].append(message.author.id)
    daily_data['votes'][vote_index] += 1
    logger.debug("Vote List after: " + str(daily_data['votes']))
    data_dict_to_json()

bot.loop.create_task(my_background_task())
bot.run(token)
