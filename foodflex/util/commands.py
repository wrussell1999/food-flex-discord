import random
import discord

import foodflex.util.data as data
import foodflex.util.config as config
import foodflex.util.static as static
import foodflex.periods.voting as voting
import foodflex.periods.results as results
import foodflex.periods.submissions as submissions
import foodflex.periods.leaderboard as leaderboard

from foodflex.util.bot import bot
from foodflex.util.logging import logger


@bot.command(description='This explains how the food flex competition works - how to submit and vote')
async def helpme(ctx):
    embed = discord.Embed(title='Help', description='Use the different channels to submit and vote!', colour=0xff0000)
    embed.set_author(name='Food Flex - How this all works')
    embed.add_field(name='Submissions', value='Submit your photos of food here! One submission per user', inline=False)
    embed.add_field(name='Voting', value='Vote with the letter corresponding to your favourite flex. Only 1 vote per user. You can\'t vote for yourself', inline=False)
    embed.add_field(name='Results', value='See who won the most recent food flex!', inline=False)
    embed.add_field(name='Scoring', value='1 point for those with the highest number of votes')
    embed.set_footer(text='For more information, contact Will R')
    await ctx.send(embed=embed)
    await ctx.message.delete()


@bot.command(description='Arguments: channel_nick, output')
async def say(ctx, channel_nick: str, output: str):
    if await bot.is_owner(ctx.author):
        if channel_nick == 'flex':
            channel = bot.get_channel(config.main_channel_id)
            await channel.send(output)
        elif channel_nick == 'leaderboard':
            channel = bot.get_channel(config.leaderboard_channel_id)
            await channel.send(output)
        await ctx.message.delete()


# @bot.group()
# async def debug(ctx):
#     if ctx.invoked_subcommand is None:
#         await ctx.send('Invalid debug command')
#
#
# @debug.command(description='Just a test to see if the bot is responding. It posts a rude quote from Ramsay.')
# async def test(ctx):
#     await ctx.send(random.choice(static.quotes['rude']))
#     await ctx.message.delete()


# @debug.command(description='Arguments: submission, voting, results')
# async def status(ctx, period: str):
#     if await bot.is_owner(ctx.author):
#         activity = discord.Activity(name='for shit food',
#                                     type=discord.ActivityType.watching)
#         if period == 'submissions':
#             activity = discord.Activity(name='people submit shit food',
#                                         type=discord.ActivityType.watching)
#             await bot.change_presence(status=discord.Status.online,
#                                       activity=activity)
#         elif period == 'voting':
#             activity = discord.Activity(name='people vote on shit food',
#                                         type=discord.ActivityType.watching)
#             await bot.change_presence(status=discord.Status.online,
#                                       activity=activity)
#         elif period == 'results':
#             await bot.change_presence(status=discord.Status.idle,
#                                       activity=activity)
#     await ctx.message.delete()


# @bot.group()
# async def data_tools(ctx):
#     if ctx.invoked_subcommand is None:
#         await ctx.send('Invalid debug command')


# @data_tools.command(description='Winner of the Food Flex so far')
# async def winner(ctx):
#     await ctx.message.delete()
#
#
# @data_tools.command(description='Shows the current daily data as dict')
# async def daily_data(ctx):
#     await ctx.send(str(data.daily_data))
#
#
# @data_tools.command(description='Arguments: submissions, voters, votes')
# async def clear(ctx, list: str):
#     if await bot.is_owner(ctx.author):
#         if list == 'submissions':
#             data.daily_data['submissions'].clear()
#             logger.debug('Submissions cleared manually')
#         elif list == 'voters':
#             data.daily_data['voters'].clear()
#             logger.debug('Voters cleared manually')
#         elif list == 'votes':
#             data.daily_data['votes'].clear()
#             logger.debug('Votes cleared manually')
#         data.save_data()
#         await ctx.message.delete()


# @data_tools.command(description='Arguments: data, score')
# async def save(ctx, file: str):
#     if await bot.is_owner(ctx.author):
#         if file == 'data':
#             data.save_data()
#         elif file == 'score':
#             data.save_leaderboard()
#         await ctx.message.delete()


# @data_tools.command(description='All the rude Gordon Ramsay quotes')
# async def rude_quotes(ctx):
#     embed = discord.Embed(title='Rude Gordon Ramsay quotes',
#                           description='All the quotes stored in ramsay_quotes.json',
#                           colour=0xff0000)
#     for index, val in enumerate(static.quotes['rude']):
#         embed.add_field(name=str(index + 1), value=val, inline=False)
#     await ctx.send(embed=embed)
#     await ctx.message.delete()
#
#
# @data_tools.command(description='Updates leaderboard')
# async def refresh_leaderboard(ctx):
#     await ctx.message.delete()
#     await leaderboard.update_leaderboard()


# @bot.group()
# async def submission(ctx):
#     if ctx.invoked_subcommand is None:
#         await ctx.send('Invalid command')


# @submission.command()
# async def open(ctx):
#     if await bot.is_owner(ctx.author):
#         await submission_command(ctx.message)
#         data.daily_data.clear()
#         logger.info('Submissions started manually')
#
#
# @submission.command()
# async def resume(ctx):
#     if await bot.is_owner(ctx.author):
#         await submission_command(ctx.message)
#         logger.info('Submissions resumed manually')


# async def submission_command(message):
#     data.shared_prefs['submissions'] = True
#     data.shared_prefs['voting'] = False
#     data.save_prefs()
#     channel = bot.get_channel(
#         config.config['food_flex_channel_id'])
#     guild = bot.get_guild(config.config['guild_id'])
#     await submissions.submission_period(channel)
#     await channel.set_permissions(guild.default_role, attach_files=True)
#     await message.delete()


# @submission.command()
# async def close(ctx):
#     if await bot.is_owner(ctx.author):
#         data.shared_prefs['submissions'] = False
#         data.shared_prefs['voting'] = False
#         data.save_prefs()
#
#         activity = discord.Activity(name='bugs get fixed',
#                                     type=discord.ActivityType.watching)
#         await bot.change_presence(status=discord.Status.online,
#                                   activity=activity)
#         embed = discord.Embed(title=static.strings['submission_closed_title'],
#                               description=static.strings['submission_closed'],
#                               colour=0xff0000)
#         channel = bot.get_channel(config.config['food_flex_channel_id'])
#
#         guild = bot.get_guild(config.config['guild_id'])
#         await channel.set_permissions(guild.default_role, attach_files=False)
#         await channel.send(embed=embed)
#         await ctx.message.delete()

@bot.command()
async def submit(ctx):
    if ctx.author.id in config.admin_ids:
        data.period = 'submissions'
        data.save_state()

        logger.debug('Submissions started manually')
        await submissions.submission_period(bot.get_channel(config.main_channel_id))

        await ctx.message.delete()

@bot.command()
async def vote(ctx):
    if ctx.author.id in config.admin_ids:
        data.period = 'voting'
        data.save_state()

        logger.debug('Voting started manually')
        await voting.voting_period(bot.get_channel(config.main_channel_id))

        await ctx.message.delete()


@bot.command(description='Results for a current day. Requires at least one voter')
async def result(ctx):
    if ctx.author.id in config.admin_ids:
        data.period = 'results'
        data.save_state()

        logger.debug('Results started manually')
        await results.results_period(bot.get_channel(config.main_channel_id))

        await ctx.message.delete()
