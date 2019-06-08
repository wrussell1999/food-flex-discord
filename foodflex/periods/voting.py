import discord
from discord.ext import commands
import datetime
import random
from builtins import bot
from ..util.data import daily_data, save_data, strings, config
from ..util import config

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
    logger.info("Vote '{}' from '{}' ({})".format( \
        message.clean_content, message.author.nick, str(message.author.id)))

    # votes must be a single letter
    if len(message.clean_content) != 1:
        await log_and_dm("Invalid vote!\nVotes must be a single letter", message.author)
        return

    # make sure votes are upper case
    vote = message.clean_content.upper()

    # convent 🅱 to B
    if message.clean_content == '🅱':
        vote = 'B'

    user_id = str(message.author.id)

    if user_id in daily_data:
        # this person has submitted/voted before
        if daily_data[user_id]['vote_letter'] == vote:
            await log_and_dm("Invalid vote!\nYou cannot vote for yourself", message.author)
            return

        if daily_data[user_id]['voted']:
            await log_and_dm("Invalid vote!\nYou have already voted", message.author)
            return
    else:
        # person has not submitted so we need to create an entry for them
        daily_data[user_id] = {
            "nick": message.author.nick,
            "submitted": False,
            "voted": False, # only set to true when they make a valid vote
            "votes": 0,
            "vote_letter": None
        }

    # create a dict that maps letters to user_ids of people who submitted
    # this could be stored somewhere and remove the need for 'vote_letter'
    # in the future
    letter_to_user_id = {}
    for user_id in daily_data:
        letter = daily_data[user_id]['vote_letter']
        if letter != None:
            letter_to_user_id[letter] = user_id

    logger.debug("Vote letter to user_id map: " + letter_to_user_id.__str__())

    # add one to the number of votes that the person we are voting for has
    try:
        user_id_voted_for = letter_to_user_id[vote]
        daily_data[user_id_voted_for]['votes'] += 1
        daily_data[user_id]['voted'] = True
        await log_and_dm("Vote has been submitted successfully for '{}'".format( \
            daily_data[user_id_voted_for]['nick']), message.author)
        save_data()
    except KeyError as e:
        # the letter voted for does not refer to anyone
        await log_and_dm("Invalid vote!\nCan't find user for letter '{}'".format( \
            vote), message.author)

async def log_and_dm(reason, person):
    await person.send(reason)
    logger.info(reason)

async def individual_vote_reminder():
    for user in daily_data:
        if daily_data[str(user)]['submitted'] and \
                not daily_data[str(user)]['voted']:
            user = bot.get_guild(
                config.config['guild_id']).get_member(
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
