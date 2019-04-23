import discord
from discord.ext import commands
import os
import datetime
import json
import asyncio
import random
import logging

logging.basicConfig(level=logging.INFO)
bot = commands.Bot(command_prefix='flex:')

logger = logging.getLogger('food-flex')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='foodflex.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

with open("data/config.json") as file:
    config = json.load(file)
    logger.debug("Config data loaded")

with open("data/quotes.json") as quote_file:
    quotes = json.load(quote_file)
    logger.debug("Quotes loaded")

with open("data/scoreboard.json") as score_file:
    overall_score = json.load(score_file)

sorted_scoreboard_dict = {}

def score_dict_to_json():
    logger.debug("'scoreboard' dumped to scoreboard.json")
    with open('data/scoreboard.json', 'w') as json_file:
        json.dump(overall_score, json_file)

temp_data = {} # daily data
with open("data/daily_data.json") as temp_file:
    temp_data = json.load(temp_file)

sorted_submissions_dict = {}

logger.debug(temp_data) # loaded
    
def data_dict_to_json():
    logger.debug("'data' dumped to daily_data.json")
    with open('data/daily_data.json', 'w') as json_file:
        json.dump(temp_data, json_file)

token = config['token_id']

@bot.event
async def on_ready(): 
    logger.debug("Food Flex is online!")

async def my_background_task():
    await bot.wait_until_ready()

    submission_channel = bot.get_channel(config['submission_channel_id'])
    voting_channel = bot.get_channel(config['voting_channel_id'])
    results_channel = bot.get_channel(config['results_channel_id'])
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
            await bot.send_message(submission_channel, embed=embed)
        elif ((hour == 00 and minute == 00) and len(temp_data['submissions']) > 1):
            await voting_period(submission_channel, voting_channel)
        elif (hour == 11 and minute == 00 and len(temp_data['submissions']) > 1):
            logger.info("1 hour left for voting")
            embed = await embed_scoreboard(temp_data['submissions'], temp_data['votes'], "1 hour left for voting", "There's still time to vote! Here are the current scores")
            embed.set_footer(text="Remember to vote for your submission to be valid!")
            await vote_reminder()      
            await bot.send_message(voting_channel, embed=embed)
        elif ((hour == 12 and minute == 00) and len(temp_data['submissions']) > 1 and len(temp_data['voters']) > 0):
            await results_period(voting_channel, submission_channel, results_channel)
        await asyncio.sleep(60) # task runs every 60 seconds

async def submission_period(submission_channel, voting_channel):
    logger.info("SUBMISSIONS")
    embed = discord.Embed(title="Submissions are open", description="Submit a picture of your cooking!", colour=0xff0000)
    await bot.send_message(submission_channel, embed=embed)
    await channel_permissions(True, False, submission_channel, voting_channel)

async def voting_period(submission_channel, voting_channel):
    logger.info("VOTING")
    embed = discord.Embed(title="VOTING!", description ="Vote for the best cooking of the day!", colour=0xff0000)
    embed.set_footer(text="Respond in the chat with the appropriate letter")
    vote_value = 'A'
    for value in temp_data['submissions']:
        user = bot.get_server(config['server_id']).get_member(str(value))
        embed.add_field(name=user.nick, value=str(vote_value), inline=True)
        vote_value = chr(ord(vote_value) + 1)    
    await bot.send_message(voting_channel, embed=embed)

    for value in temp_data['submissions']:
        temp_data['votes'].append(0)
    logger.info(str(temp_data['votes']))
    data_dict_to_json()
    await channel_permissions(False, True, submission_channel, voting_channel)

async def vote_reminder():
    logger.debug("Reminding users who submitted")
    for member_id in temp_data['submissions']:
        if member_id in temp_data['voters']:
            logger.debug(member_id + " has voted - no reminder")
        else:
            user = bot.get_server(config['server_id']).get_member(member_id)
            await bot.send_message(user, "Remember to vote for your submission to be valid!!!")
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
        user_obj = bot.get_server(config['server_id']).get_member(sorted_submissions_dict['submissions'][index])
        embed.add_field(name=user_obj.nick, value=votes_str, inline=True)
    await bot.send_message(results_channel, embed=embed)
    reset_dict()
    data_dict_to_json()
    await channel_permissions(False, False, voting_channel, submission_channel)

def reset_dict():
    temp_data['submissions'].clear()
    temp_data['votes'].clear()
    temp_data['voters'].clear()
    logger.debug("temp_data reset")

async def get_winner(results_channel):
    logger.debug("Getting Winner")
    max_vote = max(temp_data['votes'])
    if (max_vote > 0):
        winner_indexes = [i for i, j in enumerate(temp_data['votes']) if j == max_vote]
        logger.debug("index of winners: "  + str(winner_indexes))
        winner_message = ""
        sorted_submissions_dict = sort_submissions()
        winner_true = False
        while (winner_true == False):
            if (len(winner_indexes) > 1 and len(temp_data['submissions']) > 1):
                logger.debug("Multiple winners")
                winners = []
                winner_message = "Winners: "
                for index, winner_index in enumerate(winner_indexes):
                    winners.append(bot.get_server(config['server_id']).get_member(str(temp_data['submissions'][winner_index])))
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
                winner = bot.get_server(config['server_id']).get_member(str((temp_data['submissions'][winner_indexes[0]])))
                if (check_winner_vote(winner) == True):
                    update_score(winner, 1)
                    winner_message = "Winner: " + winner.nick
                    logger.info("Winner: " + str(winner.nick))
                    winner_true = True
                else:
                    await disqualify_winner(winner, winner_indexes[0])
    else:
        embed = discord.Embed(title="No winner", description="The potential winners were disqualified", colour=0xff0000)
        await bot.send_message(results_channel, embed=embed)
        winner_message = "No winner"
    return winner_message

def check_winner_vote(winner):
    if winner.id in temp_data['voters']:
        logger.debug("Winner voted - valid")
        return True
    else:
        logger.warning("Winner disqualified")
        return False

async def disqualify_winner(winner, index):
    winner_message = "Winner disqualified: " + str(winner.nick)
    embed = discord.Embed(title=winner_message, description="Winner did not vote, therefore their submission is invalid", colour=0xff0000)
    await bot.send_message(bot.get_channel(config['results_channel_id']), embed=embed)
    logger.debug("New winner selected" + str(temp_data['submissions'][index]))
    del temp_data['votes'][index]
    del temp_data['submissions'][index]


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
    sorted_submissions_dict['submissions'] = [x for _, x in sorted(zip(temp_data['votes'], temp_data['submissions']), reverse=True)]
    sorted_submissions_dict['votes'] = [x for _, x in sorted(zip(temp_data['votes'], temp_data['votes']), reverse=True)]
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
        user = bot.get_server(config['server_id']).get_member(str(val))
        score = "Score: " + str(scores[index])
        embed.add_field(name=user.nick, value=score)
    return embed

async def scoreboard(channel):
    sorted_scoreboard_dict = sort_scoreboard()
    embed = await embed_scoreboard(sorted_scoreboard_dict['users'], sorted_scoreboard_dict['scores'], "SCOREBOARD", "Scoreboard for this term")
    await bot.send_message(channel, embed=embed)

async def auto_scoreboard():
    sorted_scoreboard_dict = sort_scoreboard()
    embed = await embed_scoreboard(sorted_scoreboard_dict['users'], sorted_scoreboard_dict['scores'], "SCOREBOARD", "Scoreboard for this term")
    await bot.send_message(bot.get_channel(config['results_channel_id']), embed=embed)

async def channel_permissions(before, after, channel_before, channel_after):
    server = bot.get_server(config['server_id'])
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = before
    await bot.edit_channel_permissions(channel_before, server.default_role, overwrite)
    overwrite.send_messages = after
    await bot.edit_channel_permissions(channel_after, server.default_role, overwrite)
    logger.debug("Permissions updated")
    
@bot.event    
async def on_message(message):
    submission_channel = bot.get_channel(config['submission_channel_id'])
    voting_channel = bot.get_channel(config['voting_channel_id'])
    dev_channel = bot.get_channel(config['dev_channel_id'])
    server = bot.get_server(config['server_id'])
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
    for value in temp_data['submissions']:
        if (message.author.id == value):
            duplicate = True
    if (duplicate == False):
        temp_data['submissions'].append(message.author.id)
        logger.debug("Submission valid")
        #update_score(message.author, 1)
        await bot.send_message(submission_channel, random.choice(quotes['rude']))
        data_dict_to_json()
    elif (duplicate == True):
        logger.warning("User already submitted - submission invalid")

async def check_vote(message, voting_channel):
    logger.info("Vote by: " + str(message.author.nick))
    raw = str(message.clean_content)
    vote = raw[0]
    vote_index = ord(vote) - 65
    logger.debug("vote_index: " + str(vote_index)) # this is an index
    logger.debug("Vote List before: " + str(temp_data['votes']))
    if (vote_index < len(temp_data['submissions']) and vote_index >= 0): # Checks if it's in range
        duplicate = validate_vote(vote_index, voting_channel, message)
        if (duplicate == True): 
            logger.warn("User already voted: invalid")
        elif(duplicate == False): 
            await valid_vote(vote_index, voting_channel, message)

def validate_vote(vote_index, voting_channel, message):
    if (validate_self_vote(vote_index, voting_channel, message) == True):
        return True
    elif message.author.id in temp_data['voters']: 
        return True
    else:
        return False

def validate_self_vote(vote_index, voting_channel, message):
    if (message.author.id in temp_data['submissions']):
        voter_index = temp_data['submissions'].index(message.author.id)
        logger.debug("voter_index: " + str(voter_index))
    else:
        voter_index = -1
    if (voter_index == vote_index):
        logger.warn("Invalid vote: same submission")
        return True
    else:
        return False

async def valid_vote(vote_index, voting_channel, message):
    temp_data['voters'].append(message.author.id)
    temp_data['votes'][vote_index] += 1
    logger.debug("Vote List after: " + str(temp_data['votes']))
    data_dict_to_json()

@bot.command(pass_context=True, description="This explains how the food flex competition works - how to submit and vote")
async def helpme(ctx):
    embed = discord.Embed(title="Help", description="Use the different channels to submit and vote!", colour=0xff0000)
    embed.set_author(name="Food Flex - How this all works")
    embed.add_field(name="#submissions", value="Submit your photos of food here! One submission per user", inline=False)
    embed.add_field(name="#voting", value="Vote with the letter corresponding to your favourite flex. Only 1 vote per user. You can't vote for yourself", inline=False)
    embed.add_field(name="#results", value="See who won the most recent food flex!", inline=False)
    embed.add_field(name="Scoring", value="1 point for those with the highest number of votes")
    embed.set_footer(text="For more information, contact Will R")
    await bot.say(embed=embed)
    await bot.delete_message(ctx.message)

@bot.command(pass_context=True, description="Shows the overall score for the food flex")
async def score(ctx):
    await scoreboard(ctx.message.channel)
    await bot.delete_message(ctx.message)

@bot.command(pass_context=True, description="Winner of the Food Flex so far")
async def winner(ctx):
    embed = discord.Embed(title="Winners", description="Highest score for term 2", colour=0xff0000)
    embed.set_footer(text="It's all to play for...")
    max_vote = max(overall_score['score'])
    value_str = "Score: " + str(max_vote)
    winner_indexes = [i for i, j in enumerate(overall_score['score']) if j == max_vote]
    if (len(winner_indexes) > 1):
        winners = []
        for index, winner_index in enumerate(winner_indexes):
            winners.append(bot.get_server(config['server_id']).get_member(str(overall_score['users'][winner_index])))
        for index, member in enumerate(winners):
            embed.add_field(name=member.nick, value=value_str)
        logger.debug("Command: Multiple winners")
    else:
        winner = bot.get_server(config['server_id']).get_member(str((overall_score['users'][winner_indexes[0]])))
        embed.add_field(name=winner.nick, value=value_str)
        logger.debug("Command: Single winner")
    logger.debug("Winner command")
    await bot.say(embed=embed)
    await bot.delete_message(ctx.message)

@bot.command(pass_context=True, description="Just a test to see if the bot is responding. It posts a rude quote from Ramsay.")
async def test(ctx):
    await bot.say(random.choice(quotes['rude']))
    await bot.send_message(ctx.message.author, "Test")
    await bot.delete_message(ctx.message)

@bot.command(pass_context=True, description="All the rude Gordon Ramsay Quotes")
async def rude_quotes(ctx):
    embed = discord.Embed(title="Rude Gordon Ramsay Quotes", description="All the quotes stored in ramsay_quotes.json", colour=0xff0000)
    for index, val in enumerate(quotes['rude']):
        embed.add_field(name=str(index + 1), value=val, inline=False)
    await bot.say(embed=embed)
    await bot.delete_message(ctx.message)

@bot.command(pass_context=True)
async def say(ctx, channel: str, output: str):
    if (ctx.message.author.id == config['admin_id']):
        if (channel == "main"):
            food_chat = bot.get_channel(config['food_chat_id'])
            await bot.send_message(food_chat, output)
        elif (channel == "submission"):
            submission_channel = bot.get_channel(config['submission_channel_id'])
            await bot.send_message(submission_channel, output)  
        elif (channel == "voting"):
            voting_channel = bot.get_channel(config['voting_channel_id'])
            await bot.send_message(voting_channel, output)  
        elif (channel == "results"):
            results_channel = bot.get_channel(config['results_channel_id'])
            await bot.send_message(results_channel, output)  
        await bot.delete_message(ctx.message)
@bot.command(pass_context=True)
async def warwick_term2(ctx):
    embed = discord.Embed(title="Warwick Term 2 Leaderboard",
                          description="Overall Food Flex Scores for Term 2, Year 1", colour=0xff0000)
    embed.add_field(name="1st: James", value="Score: 12", inline=False)
    embed.add_field(name="2nd: Dan", value="Score: 10", inline=False)
    embed.add_field(name="3rd: Ali", value="Score: 1", inline=False)
    embed.add_field(name="3rd: Harry", value="Score: 1", inline=False)
    embed.add_field(name="Honourable mention: Joe", value="He tried", inline=False)
    await bot.say(embed=embed)
    await bot.delete_message(ctx.message)

@bot.command(pass_context=True)
async def final_score(ctx):
    embed = discord.Embed(title="Term 2 Leaderboard",
                          description="Overall Food Flex Scores for Term 2, Year 1", colour=0xff0000)
    embed.add_field(name="1st: James", value="Score: 12", inline=False)
    embed.add_field(name="2nd: Dan", value="Score: 10", inline=False)
    embed.add_field(name="3rd: Will", value="Score: 9", inline=False)
    await bot.say(embed=embed)
    await bot.delete_message(ctx.message)

@bot.group(pass_context=True)
async def debug(ctx):
    if (ctx.invoked_subcommand is None):
        await bot.say('Invalid debug command')

@debug.command(pass_context=True, description="Shows the current daily data as dict")
async def data(ctx):
    embed = discord.Embed(title="data.json", description="", colour=0xff0000)
    embed.add_field(name="Submissions", value=temp_data['submissions'])
    embed.add_field(name="Voters", value=temp_data['voters'])
    embed.add_field(name="Votes", value=temp_data['votes'])
    await bot.say(embed=embed)
    
@debug.command(pass_context=True)
async def submissions(ctx):
    if (ctx.message.author.id == config['admin_id']):
        await submission_period(bot.get_channel(config['submission_channel_id']), bot.get_channel(config['voting_channel_id']))
        reset_dict()
        logger.info("Submissions started manually")
        await bot.delete_message(ctx.message)

@debug.command(pass_context=True)
async def voting(ctx):
    if (ctx.message.author.id == config['admin_id']):
        await voting_period(bot.get_channel(config['submission_channel_id']), bot.get_channel(config['voting_channel_id']))
        logger.debug("Voting started manually")
        await bot.delete_message(ctx.message)

@debug.command(pass_context=True)
async def results(ctx):
    if (ctx.message.author.id == config['admin_id']):
        await results_period(bot.get_channel(config['voting_channel_id']), bot.get_channel(config['submission_channel_id']), bot.get_channel(config['results_channel_id']))
        logger.debug("Results started manually")
        await bot.delete_message(ctx.message)

@debug.command(pass_context=True)
async def clear(ctx, list: str):
    if (ctx.message.author.id == config['admin_id']):
        if (list == "submissions"):
            temp_data['submissions'].clear()
            logger.debug("Submissions cleared manually")
        elif(list == "voters"):
            temp_data['voters'].clear()
            logger.debug("Voters cleared manually")
        elif(list == "votes"):
            temp_data['votes'].clear()
            logger.debug("Votes cleared manually")
        data_dict_to_json()
        await bot.delete_message(ctx.message)

@debug.command(pass_context=True)
async def force_json_dump(ctx, file: str):
    if (ctx.message.author.id == config['admin_id']):
        if (file == "data"):
            data_dict_to_json()
        elif (file == "score"):
            score_dict_to_json()
        await bot.delete_message(ctx.message)

bot.loop.create_task(my_background_task())
bot.run(token)