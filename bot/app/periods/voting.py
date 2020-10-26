import discord
import builtins
import app.data.images as images
import app.data.firestore as data
import app.data.static as static
import app.data.leaderboard as leaderboard
from app.util.logging import logger

async def voting_period():
    logger.info('// Now in VOTING period //')
    logger.info('Creating voting key...')

    # we need to build voting_map map first
    data.build_voting_map()

    logger.debug('Creating (url, letter) pairs for submissions...')
    submissions = []
    # create (image_url, letter) pair list
    for letter in data.voting_map:
        user_id = data.voting_map[letter]
        image_url = data.weekly_data[user_id]['image_url']
        submissions.append((image_url, letter))

    # sort submissions by alphabetical key
    submissions.sort(key=lambda tuple: tuple[1], reverse=False)

    logger.debug('Generating images...')
    # process images
    image_objects = []
    for (image_url, letter) in submissions:
        buffer = images.process_image(image_url, letter)
        image_objects.append(discord.File(buffer, filename=f'{letter}.png'))

    # announce voting is open
    await main_channel.send(static.strings['voting_open_title'])

    logger.debug('Uploading images...')
    # upload images
    for image in image_objects:
        await main_channel.send(file=image)

    # remind people how to vote and change presence
    await main_channel.send(static.strings['voting_open_footer'])

    activity = discord.Activity(name='people vote on shit food',
                                type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    logger.info('Done, voting key posted')

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

    if user_id in data.weekly_data:
        # This person has submitted/voted before
        try:
            voting_for = data.voting_map[vote]
            if voting_for == user_id:
                await log_and_dm('Invalid vote', 'You cannot vote for yourself',
                                 message.author)
                return
        except KeyError:
            pass

        if data.weekly_data[user_id]['voted']:
            await log_and_dm('Invalid vote', 'You have already voted', message.author)
            return
    else:
        # Person has not submitted so we need to create an entry for them
        data.weekly_data[user_id] = {
            u'nick': message.author.display_name,
            u'submitted': False,
            u'voted': False,  # only set to true when they make a valid vote
            u'votes': 0
        }

    # Add one to the number of votes that the person we are voting for has
    try:
        user_id_voted_for = data.voting_map[vote]
        data.weekly_data[user_id_voted_for]['votes'] += 1
        data.weekly_data[user_id]['voted'] = True
        nickname = data.weekly_data[user_id_voted_for]['nick']
        await log_and_dm('Vote successful!', f'Vote has been submitted successfully for \'{nickname}\'', message.author)
        data.update_weekly_document()
        data.update_voting_map()
    except KeyError:
        # The letter voted for does not refer to anyone
        await log_and_dm('Invalid vote', f'Can\'t find user for letter \'{vote}\'', message.author)

async def log_and_dm(title, reason, person):
    embed = discord.Embed(
        title=title,
        description=reason,
        colour=0xff0000)
    await person.send(embed=embed)
    logger.info(reason + ', ' + title)

async def voting_reminder():
    embed = discord.Embed(title=static.strings['voting_reminder_title'],
                          description=static.strings['voting_reminder'])

    # Gets users as a list of tuples (user, score)
    users = []
    for key in data.weekly_data:
        if data.weekly_data[key]['submitted']:
            tuple = (data.weekly_data[key]['nick'], data.weekly_data[key]['votes'])
            users.append(tuple)
    users.sort(key=lambda tuple: tuple[1], reverse=True)

    # Create embed and add people to it
    embed = discord.Embed(title='Current scores', description='There\'s still time to vote!', colour=0xff0000)

    # Add users to embed and send
    for (nick, vote) in users:
        embed.add_field(name=nick, value=vote, inline=False)
    await main_channel.send(embed=embed)

async def individual_vote_reminder():
    for user in data.weekly_data:
        if data.weekly_data[user]['submitted'] and \
                not data.weekly_data[user]['voted']:
            member = builtins.guild.get_member(int(user))

            if member is None:
                logger.warn(f'Unable to get user object for \'{user}\', skipping their vote reminder')
                continue

            embed = discord.Embed(title=static.strings['voting_dm_reminder_title'],
                                  description=static.strings['voting_dm_reminder'],
                                  colour=0xff0000)
            embed.set_footer(text=static.strings['voting_dm_reminder_footer'])
            await member.send(embed=embed)
            logger.debug(f'Vote reminder sent for \'{member.display_name}\' ({member.id})')
