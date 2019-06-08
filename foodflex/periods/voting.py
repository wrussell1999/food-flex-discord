import discord
from discord.ext import commands
import datetime
import random
from builtins import bot
from ..util.data import daily_data, data_dict_to_json, strings, config
from ..util import config
from ..util.setup_period import *

logger = config.initilise_logging()


async def voting_period(channel):
    logger.info("VOTING")
    activity = discord.Activity(name="people vote on shit food",
                                type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    embed = discord.Embed(title="Voting is open",
                          description="Vote for the best cooking of the day!",
                          colour=0xff0000)
    embed.set_footer(text="Respond in the chat with the appropriate letter")

    for value in daily_data:
        embed.add_field(name=daily_data[str(value)]['nick'],
                        value=daily_data[str(value)]['vote_letter'],
                        inline=False)

    await channel.send(embed=embed)


async def check_vote(message):
    logger.info("Vote by: " + str(message.author.nick))

    vote = message.clean_content[0]
    if message.clean_content in [':b:', '🅱️']:
        vote = 'B'

    user_id = str(message.author.id)

    if user_id not in daily_data:
        user = bot.get_guild(
            config.config['server_id']).get_member(message.author.id)
        print(user.nick)
        daily_data[user_id] = {
            "nick": str(user.nick),
            "submitted": False,
            "voted": True,
            "votes": 0,
            "vote_letter": None
        }
    if not daily_data[user_id]['voted'] or \
            daily_data[user_id]['vote_letter'] is not vote:

        daily_data[user_id]['voted'] = True
        for user in daily_data:
            if daily_data[str(user)]['vote_letter'] == vote:
                daily_data[str(user)]['votes'] += 1
            
        save_data()
        await message.author.send(
            "Your vote has been submitted successfully")
    else:
        await message.author.send("Invalid vote!")


async def individual_vote_reminder():
    for user in daily_data:
        if daily_data[str(user)]['submitted'] and \
                not daily_data[str(user)]['voted']:
            user = bot.get_guild(
                config.config['server_id']).get_member(
                str(user))
            embed = discord.Embed(title="REMINDER!",
                                  description="Remember to vote for " +
                                  "your submission to be valid!!!")
            embed.set_footer(text="You will be disqualified if you don't vote")
            await user.send(embed=embed)
            logger.debug("Vote reminder sent for " + str(user.nick))


@bot.command()
async def voting(ctx):
    if await bot.is_owner(ctx.author):
        await voting_period(bot.get_channel(
            config.config['food_flex_channel_id']))
        logger.debug("Voting started manually")
        await ctx.message.delete()
