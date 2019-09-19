import discord

import foodflex.util.data as data
import foodflex.util.config as config
import foodflex.periods.leaderboard as leaderboard

from foodflex.util.logging import logger
from foodflex.util.bot import bot, __version__


async def results_period():
    logger.info('// Now in RESULTS period //')
    activity = discord.Activity(
        name='for shit food', type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.idle, activity=activity)

    logger.info('Preparing reuslts...')
    # Get list of users (tuples) who submitted (nick, votes)
    users = []
    for user in data.participants:
        if data.participants[user]['submitted']:
            tuple = (data.participants[user]['nick'], data.participants[user]['votes'])
            users.append(tuple)
    users.sort(key=lambda tuple: tuple[1], reverse=True)

    # Get the winner(s) as a string
    winner_message = await get_winner(main_channel)

    embed = discord.Embed(title='Results', description='', colour=0xff0000)
    embed.set_author(name=winner_message)

    # Add users to embed
    for user in users:
        votes = 'Votes: ' + str(user[1])
        embed.add_field(name=user[0], value=votes, inline=False)

    await main_channel.send(embed=embed)
    logger.info('Results posted')
    await leaderboard.update_leaderboard()


async def get_winner():
    # Get a list of potential winners
    users = []
    for index, key in enumerate(data.participants):
        if data.participants[key]['submitted'] and data.participants[key]['voted']:
            tuple = (data.participants[key]['nick'],
                     data.participants[key]['votes'],
                     list(data.participants.keys())[index])
            users.append(tuple)
    users.sort(key=lambda tuple: tuple[1], reverse=True)

    if len(users) == 0:
        embed = discord.Embed(
            title='No winner',
            description='No users both submitted and voted',
            colour=0xff0000)
        await main_channel.send(embed=embed)
        return 'No winner'

    # Check if there are any potential winners in the list
    max_votes = users[0][1]
    if len(users) == 0 or max_votes == 0:
        embed = discord.Embed(
            title='No winner',
            description='The potential winners were disqualified',
            colour=0xff0000)
        await main_channel.send(embed=embed)
        return 'No winner'

    # Get the potential winners as a single string
    winner_message = 'Winners: '
    for user in users:
        if user[1] != max_votes:
            users.remove(user)
        else:
            # Adds user to string, and updates leaderboard score
            winner_message += user[0] + ', '
            leaderboard.update_score(user[2], user[0])
    return winner_message
