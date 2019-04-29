import discord
from discord.ext import commands
import datetime
import random
from builtins import bot
from data import *
import config

logger = config.initilise_logging()

async def channel_permissions(before, after, channel_before, channel_after):
    guild = bot.get_guild(config.config['server_id'])
    await channel_before.set_permissions(guild.default_role, send_messages=before)
    await channel_after.set_permissions(guild.default_role, send_messages=after)
    logger.debug("Permissions updated")

@bot.group()
async def debug(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid debug command')

@debug.command()
async def submissions(ctx):
    if await bot.is_owner(ctx.author):
        await submission_period(bot.get_channel(config.config['submission_channel_id']), bot.get_channel(config.config['voting_channel_id']))
        reset_dict()
        logger.info("Submissions started manually")
        await ctx.message.delete()

@debug.command()
async def voting(ctx):
    if await bot.is_owner(ctx.author):
        await voting_period(bot.get_channel(config.config['submission_channel_id']), bot.get_channel(config.config['voting_channel_id']))
        logger.debug("Voting started manually")
        await ctx.message.delete()

@debug.command()
async def results(ctx):
    if await bot.is_owner(ctx.author) and len(daily_data['voters']) != 0:
        await results_period(bot.get_channel(config.config['voting_channel_id']), bot.get_channel(config.config['submission_channel_id']), bot.get_channel(config.config['results_channel_id']))
        logger.debug("Results started manually")
        await ctx.message.delete()

@bot.command(description="Shows the overall score for the food flex")
async def score(ctx):
    await scoreboard(ctx.channel)
    await ctx.message.delete()
