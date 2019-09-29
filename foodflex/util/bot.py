import builtins
from discord.ext import commands

import foodflex.util.config as config
from foodflex.util.logging import logger

builtins.__version__ = '2.0.0'

logger.debug(f'Creating bot (cmd prefix \'{config.command_prefix}\')...')
builtins.bot = commands.Bot(command_prefix=config.command_prefix)

@bot.event
async def on_ready():
    global main_channel, leaderboard_channel
    logger.debug('Finding text channels...')

    builtins.main_channel = bot.get_channel(config.main_channel_id)
    builtins.leaderboard_channel = bot.get_channel(config.leaderboard_channel_id)

    logger.info('Food Flex is online!')
