__version__ = '2.0.0'

from discord.ext import commands

import foodflex.util.config as config
from foodflex.util.logging import logger

logger.debug(f'Creating bot (cmd prefix \'{config.command_prefix}\')...')
bot = commands.Bot(command_prefix=config.command_prefix)
