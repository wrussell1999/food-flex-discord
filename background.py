import discord
from discord.ext import commands
import datetime
import random
from data import *
import config
from builtins import bot

sorted_scoreboard_dict = {}
sorted_submissions_dict = {}
logger = config.initilise_logging()

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

@bot.group(pass_context=True)
async def debug(ctx):
    if (ctx.invoked_subcommand is None):
        await bot.ctx('Invalid debug command')

@debug.command(pass_context=True)
async def submissions(ctx):
    if (ctx.author.id == config.config['admin_id']):
        await submission_period(bot.get_channel(config.config['submission_channel_id']), bot.get_channel(config.config['voting_channel_id']))
        reset_dict()
        logger.info("Submissions started manually")
        await ctx.message.delete()

@debug.command(pass_context=True)
async def voting(ctx):
    if (ctx.author.id == config.config['admin_id']):
        await voting_period(bot.get_channel(config.config['submission_channel_id']), bot.get_channel(config.config['voting_channel_id']))
        logger.debug("Voting started manually")
        await ctx.message.delete()

@debug.command(pass_context=True)
async def results(ctx):
    if (ctx.author.id == config.config['admin_id']):
        await results_period(bot.get_channel(config.config['voting_channel_id']), bot.get_channel(config.config['submission_channel_id']), bot.get_channel(config.config['results_channel_id']))
        logger.debug("Results started manually")
        await ctx.message.delete()

@bot.command(pass_context=True, description="Shows the overall score for the food flex")
async def score(ctx):
    await scoreboard(ctx.channel)
    await ctx.message.delete()
