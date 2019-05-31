import discord
from discord.ext import commands
import datetime
import random
from builtins import bot
from .data import *
from . import config

logger = config.initilise_logging()

async def channel_permissions(before, after, channel_before, channel_after):
    guild = bot.get_guild(config.config['server_id'])
    await channel_before.set_permissions(guild.default_role, send_messages=before)
    await channel_after.set_permissions(guild.default_role, send_messages=after)
    logger.debug("Permissions updated")

def reset_daily_data():
    daily_data['submissions'].clear()
    daily_data['votes'].clear()
    daily_data['voters'].clear()

