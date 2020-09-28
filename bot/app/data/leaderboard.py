import os
import discord
import datetime
import builtins
import app.data.firestore as data
from app.util.logging import logger

def update_score(user_id, user_nick):
    # Checks if the user is already on the leaderboard
    if user_id not in data.leaderboard:
        # Adds user to leaderboard
        data.leaderboard[user_id] = {
            'nick': user_nick,
            'score': 1
        }
    else:
        data.leaderboard[user_id]['score'] += 1

async def update_leaderboard():
    # Gets a list of users and scores (as tuple in descending order)
    users = [(data.leaderboard[key]['nick'], data.leaderboard[key]['score'])
             for key in data.leaderboard]
    users.sort(key=lambda tuple: tuple[1], reverse=True)

    # Checks if the leaderboard has already been posted

    if "leaderboard_message_id" not in data.state and os.getenv("LEADERBOARD_MESSAGE_ID") == None:
        # Creates new leaderboard
        logger.info("Make new leaderboard message")
        embed = get_embed(users)
        await builtins.leaderboard_channel.send(embed=embed)
        leaderboard_id = leaderboard_channel.last_message_id
        builtins.leaderboard_message = await builtins.leaderboard_channel.fetch_message(leaderboard_id)
        data.state['leaderboard_message_id'] = leaderboard_id
        data.update_state()
    else:
        # Edits and existing one
        logger.info("Edit leaderboard message")
        embed = get_embed(users)
        await builtins.leaderboard_message.edit(embed=embed)
    data.update_leaderboard()

def get_embed(users):
    # Gets the date
    now = datetime.datetime.now()
    date_str = 'Updated: ' + \
        str(now.day) + '/' + str(now.month) + '/' + str(now.year)

    # Makes an embed
    embed = discord.Embed(
        title='Leaderboard',
        description='Overall scores this term',
        colour=0xff0000)
    embed.set_footer(text=date_str)
    # Adds the users to the embed
    for value in users:
        score = 'Score: ' + str(value[1])
        embed.add_field(name=value[0], value=score, inline=False)
    return embed
