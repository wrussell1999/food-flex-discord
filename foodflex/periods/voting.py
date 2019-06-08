import discord
from discord.ext import commands
import datetime
import random
from builtins import bot
import foodflex.util.data as data
import foodflex.util.config as config
import foodflex.periods.leaderboard as leaderboard

logger = config.initilise_logging()


async def voting_period(channel):
    logger.info("VOTING")
    activity = discord.Activity(name="people vote on shit food",
                                type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    embed = discord.Embed(title=data.strings['voting_open_title'],
                          description=data.strings['voting_open'],
                          colour=0xff0000)
    embed.set_footer(text=data.strings['voting_open_footer'])

    for value in data.daily_data:
        embed.add_field(name=data.daily_data[str(value)]['nick'],
                        value=data.daily_data[str(value)]['vote_letter'],
                        inline=False)

    await channel.send(embed=embed)


async def check_vote(message):
    logger.info("Vote by: " + str(message.author.nick))

    vote = message.clean_content[0]
    if message.clean_content in [':b:', '🅱️']:
        vote = 'B'

    user_id = str(message.author.id)

    if user_id not in data.daily_data:
        user = bot.get_guild(
            config.config['guild_id']).get_member(message.author.id)
        data.daily_data[user_id] = {
            "nick": str(user.nick),
            "submitted": False,
            "voted": True,
            "votes": 0,
            "vote_letter": None
        }
    else:
        if not data.daily_data[user_id]['voted'] or \
                data.daily_data[user_id]['vote_letter'] is not vote:

            data.daily_data[user_id]['voted'] = True
            for user in data.daily_data:
                if data.daily_data[str(user)]['vote_letter'] == vote:
                    data.daily_data[str(user)]['votes'] += 1

            save_data()
            await message.author.send(data.strings['voting_success'])
        else:
            await message.author.send(data.strings['voting_fail'])

async def voting_reminder():
    channel = bot.get_channel(config.config['food_flex_channel_id'])
    embed = discord.Embed(title=data.strings['voting_reminder_title'],
                          description=data.strings['voting_reminder'])

    # Gets users as a list of tuples (user, score)
    users = [(data.leaderboard_data[key]['nick'],
             data.leaderboard_data[key]['score'])
             for key in data.leaderboard_data]
    users.sort(key=lambda tuple: tuple[1], reverse=True)

    # Gets the embed with users in it
    embed = await leaderboard.get_embed(users)
    embed.set_footer(
        text="")
    await channel.send(embed=embed)

async def individual_vote_reminder():
    for user in data.daily_data:
        if data.daily_data[str(user)]['submitted'] and \
                not data.daily_data[str(user)]['voted']:
            user = bot.get_guild(
                config.config['guild_id']).get_member(
                str(user))
            embed = discord.Embed(title=data.strings['voting_dm_reminder_title'],
                                  description=data.strings['voting_dm_reminder'])
            embed.set_footer(text=data.strings['voting_dm_reminder_footer'])
            await user.send(embed=embed)
            logger.debug("Vote reminder sent for " + str(user.nick))


@bot.command()
async def voting(ctx):
    if await bot.is_owner(ctx.author):
        await voting_period(bot.get_channel(
            config.config['food_flex_channel_id']))
        logger.debug("Voting started manually")
        await ctx.message.delete()
