import discord
from discord.ext import commands
import datetime
import random
from builtins import bot
import foodflex.util.data as data
import foodflex.util.config as config

logger = config.initilise_logging()


async def submission_period(channel):
    logger.info('SUBMISSIONS')
    activity = discord.Activity(name=data.quotes['submission_open_activity'],
                                type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    embed = discord.Embed(title=data.quotes['submission_open_title'],
                          description=data.quotes['submission_open'],
                          colour=0xff0000)
    await channel.send(embed=embed)


async def process_submission(message, channel):
    user_id_key = str(message.author.id)
    if str(message.author.id) in data.daily_data:
        logger.info('Submission invalid')
    else:
        data.daily_data[user_id_key] = {
            'nick': str(message.author.nick),
            'submitted': True,
            'voted': False,
            'votes': 0,
            'vote_letter': chr(ord('A') + len(data.daily_data))
        }
        await channel.send(random.choice(data.quotes['rude']))
        save_data()
        logger.info('Submission valid')


async def submission_reminder():
    channel = bot.get_channel(config.config['food_flex_channel_id'])
    embed = discord.Embed(title=data.strings['submission_reminder_title'],
                          description=data.strings['submission_reminder'],
                          colour=0xff0000)
    await channel.send(embed=embed)


@bot.group()
async def submissions(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid command')


@submissions.command()
async def open(ctx):
    if await bot.is_owner(ctx.author):
        await submission_command(ctx.message)
        data.daily_data.clear()
        logger.info('Submissions started manually')


@submissions.command()
async def resume(ctx):
    if await bot.is_owner(ctx.author):
        await submission_command(ctx.message)
        logger.info('Submissions resumed manually')


async def submission_command(message):
    channel = bot.get_channel(
        config.config['food_flex_channel_id'])
    guild = bot.get_guild(config.config['guild_id'])
    await channel.set_permissions(guild.default_role, attach_files=True)
    await submission_period(channel)
    message.delete()


@submissions.command()
async def close(ctx):
    if await bot.is_owner(ctx.author):
        activity = discord.Activity(name='bugs get fixed',
                                    type=discord.ActivityType.watching)
        await bot.change_presence(status=discord.Status.online,
                                  activity=activity)
        embed = discord.Embed(title=data.strings['submission_closed_title'],
                              description=data.strings['submission_closed'],
                              colour=0xff0000)
        channel = bot.get_channel(config.config['food_flex_channel_id'])

        guild = bot.get_guild(config.config['guild_id'])
        await channel.set_permissions(guild.default_role, attach_files=False)
        await channel.send(embed=embed)
        ctx.message.delete()
