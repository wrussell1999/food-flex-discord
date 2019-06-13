import discord
from discord.ext import commands
from builtins import bot
import foodflex.util.data as data
import foodflex.util.config as config
import foodflex.periods.leaderboard as leaderboard

logger = config.initilise_logging()


async def voting_period(channel):
    logger.info("VOTING")

    # we need to build letter_to_user_id map first
    await build_voting_map()

    # create message to hold key for voting
    embed = discord.Embed(title=data.strings['voting_open_title'],
                          description=data.strings['voting_open'],
                          colour=0xff0000)

    # sort voting key alphabetically and put in into message
    submissions = []
    for letter in data.letter_to_user_id:
        user_id = data.letter_to_user_id[letter]
        nick = data.daily_data[user_id]['nick']
        submissions.append((nick, letter))

    submissions.sort(key=lambda tuple: tuple[1], reverse=False)

    for (nick, letter) in submissions:
        embed.add_field(name=nick, value=letter, inline=False)

    # when everything has been prepared, announce voting is open and post
    # voting key
    activity = discord.Activity(name="people vote on shit food",
                                type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    embed.set_footer(text=data.strings['voting_open_footer'])
    await channel.send(embed=embed)


async def check_vote(message):
    user_id = str(message.author.id)

    # Votes must be a single letter
    if len(message.clean_content) != 1:
        return

    # Make sure votes are upper case
    vote = message.clean_content.upper()

    # Convent 🅱 to B
    if message.clean_content == '🅱':
        vote = 'B'

    logger.debug("Using letter_to_user_id map: " +
                 data.letter_to_user_id.__str__())

    if user_id in data.daily_data:
        # This person has submitted/voted before
        try:
            voting_for = data.letter_to_user_id[vote]
            if voting_for == user_id:
                await log_and_dm("Invalid vote", "You cannot vote for yourself",
                                 message.author)
                return
        except KeyError:
            pass

        if data.daily_data[user_id]['voted']:
            await log_and_dm("Invalid vote", "You have already voted", message.author)
            return
    else:
        # Person has not submitted so we need to create an entry for them
        data.daily_data[user_id] = {
            "nick": message.author.nick,
            "submitted": False,
            "voted": False,  # only set to true when they make a valid vote
            "votes": 0
        }

    # Add one to the number of votes that the person we are voting for has
    try:
        user_id_voted_for = data.letter_to_user_id[vote]
        data.daily_data[user_id_voted_for]['votes'] += 1
        data.daily_data[user_id]['voted'] = True
        await log_and_dm("Vote successful!", "Vote has been submitted successfully for '{}'".format( \
            data.daily_data[user_id_voted_for]['nick']), message.author)
        data.save_data()
    except KeyError:
        # The letter voted for does not refer to anyone
        await log_and_dm("Invalid vote", "Can't find user for letter '{}'".format(
            vote), message.author)


async def log_and_dm(title, reason, person):
    embed = discord.Embed(
        title=title,
        description=reason,
        colour=0xff0000)
    await person.send(embed=embed)
    logger.info(reason)


async def build_voting_map():
    counter = 0
    logger.debug("Building letter_to_user_id map...")

    # ensure letter_to_user_id map is empty
    if len(data.letter_to_user_id) != 0:
        logger.warn("letter_to_user_id map has not been cleared, clearing now")
        data.letter_to_user_id.clear()

    # assign a letter to every person who has submitted
    for user_id in data.daily_data:
        if data.daily_data[user_id]['submitted']:
            assigned_letter = chr(ord('A') + counter)
            counter += 1
            logger.debug('Assigned letter \'{}\' to user_id \'{}\''.format(
                        assigned_letter, user_id))
            data.letter_to_user_id[assigned_letter] = user_id

    logger.debug("Generated letter_to_user_id map: " +
                 data.letter_to_user_id.__str__())
    data.save_data()

async def voting_reminder():
    channel = bot.get_channel(config.config['food_flex_channel_id'])
    embed = discord.Embed(title=data.strings['voting_reminder_title'],
                          description=data.strings['voting_reminder'])

    # Gets users as a list of tuples (user, score)
    users = []
    for key in data.daily_data:
        if data.daily_data[key]['submitted']:
            tuple = (data.daily_data[key]['nick'], data.daily_data[key]['votes'])
            users.append(tuple)
    users.sort(key=lambda tuple: tuple[1], reverse=True)

    # Create embed and add people to it
    embed = discord.Embed(title="Current scores", description="There's still time to vote!", colour=0xff000)

    # Add users to embed and send
    for (nick, vote) in users:
        embed.add_field(name=nick, value=vote, inline=False)
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
