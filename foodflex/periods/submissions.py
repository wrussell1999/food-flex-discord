import discord
from discord.ext import commands
import datetime
import random
from builtins import bot
from ..util.data import daily_data, quotes, save_data, letter_to_user_id
from ..util import config

logger = config.initilise_logging()

async def submission_period(channel):
    logger.info('SUBMISSIONS')
    activity = discord.Activity(name='people submit shit food',
                                type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    embed = discord.Embed(title='Submissions are open',
                          description='Submit a picture of your cooking!',
                          colour=0xff0000)
    await channel.send(embed=embed)


async def process_submission(message, channel):
    user_id = str(message.author.id)
    if user_id in daily_data:
        logger.info('Submission invalid')
    else:
        new_letter = chr(ord('A') + len(daily_data))
        daily_data[user_id] = {
            'nick': message.author.nick,
            'submitted': True,
            'voted': False,
            'votes': 0
        }
        letter_to_user_id[new_letter] = user_id
        await channel.send(random.choice(quotes['rude']))
        save_data()
        logger.info('Submission valid, assigned letter \'{}\''.format(new_letter))

@bot.group()
async def submissions(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid command')


@submissions.command()
async def open(ctx):
    if await bot.is_owner(ctx.author):
        await submission_command(ctx.message)
        daily_data.clear()
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
        embed = discord.Embed(title='Submissions are closed',
                              description='We are currently working hard to ' +
                              'fix some problems! Check back later!',
                              colour=0xff0000)
        channel = bot.get_channel(config.config['food_flex_channel_id'])

        guild = bot.get_guild(config.config['guild_id'])
        await channel.set_permissions(guild.default_role, attach_files=False)
        await channel.send(embed=embed)
        ctx.message.delete()
