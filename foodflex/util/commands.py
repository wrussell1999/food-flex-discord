import json
import discord
import subprocess

import foodflex.util.data as data
import foodflex.util.config as config
import foodflex.util.static as static
import foodflex.periods.voting as voting
import foodflex.periods.results as results
import foodflex.periods.submissions as submissions
import foodflex.periods.leaderboard as leaderboard

from foodflex.util.logging import logger
from foodflex.util.bot import bot, __version__

# to use any command, the user must be in the admin list
@bot.check
async def is_admin(ctx):
    authorised = ctx.author.id in config.admin_ids
    if not authorised:
        logger.warn(f'Unauthorised user \'{ctx.author.display_name}\' ({ctx.author.id}) tried to use command')
    return authorised

# handle any errors that commands produce
@bot.event
async def on_command_error(ctx, error):
    # CheckFailure is an auth error which we already log
    if not isinstance(error, discord.ext.commands.CheckFailure):
        logger.debug(f'error: {error}')

# delete the message that successfully invoked a command
@bot.after_invoke
async def after_invoke(ctx):
    await ctx.message.delete()


@bot.command(description='Get version number and git commit')
async def version(ctx):
    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
    except subprocess.CalledProcessError:
        commit = 'unknown, could not run git'

    await ctx.send(f'Food Flex v{__version__} [commit {commit}]')


@bot.command(description='Dump state into the chat')
async def state(ctx):
    state = {
        "participants": data.participants,
        "voting_map": data.voting_map,
        "period": data.period,
        "mode": data.mode
    }

    as_json = json.dumps(state, indent=2)
    await ctx.send(f'```json\n{as_json}```')


@bot.command(description='Switch to automatic time-based control')
async def automatic(ctx):
    data.set_mode('automatic')
    await ctx.send('Now in automatic mode')


@bot.command(description='Start submissions period')
async def submit(ctx):
    data.change_period('submissions', manual_change=True)
    await submissions.submission_period()
    await ctx.send('Manually switched to \'submissions\' mode')


@bot.command(description='Start voting period')
async def vote(ctx):
    data.change_period('voting', manual_change=True)
    await voting.voting_period()
    await ctx.send('Manually switched to \'voting\' mode')


@bot.command(description='Start results period')
async def result(ctx):
    data.change_period('results', manual_change=True)
    await results.results_period()
    await ctx.send('Manually switched to \'results\' mode')
