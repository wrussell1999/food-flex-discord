import discord
from discord.ext import commands
import datetime
import random
from builtins import bot
from .data import *
from . import config

logger = config.initilise_logging()

def reset_daily_data():
    daily_data['submissions'].clear()
    daily_data['votes'].clear()
    daily_data['voters'].clear()
