import os
import json
import discord
import subprocess
import foodflex.data.firestore as data
import foodflex.data.static as static
import foodflex.periods.voting as voting
import foodflex.periods.results as results
import foodflex.periods.submissions as submissions
import foodflex.data.leaderboard as leaderboard
from foodflex.util.logging import logger

# handle any errors that commands produce
admin_role_id = int(os.getenv('ADMIN_ROLE_ID'))

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
@commands.has_role(admin_role_id)
async def version(ctx):
    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
    except subprocess.CalledProcessError:
        commit = 'unknown, could not run git'

    await ctx.send(f'Food Flex v{__version__} [commit {commit}]')

@bot.command(description='Dump state into the chat')
@commands.has_role(admin_role_id)
async def state(ctx):
    state = {
        "participants": data.participants,
        "voting_map": data.voting_map,
        "period": data.period,
    }

    as_json = json.dumps(state, indent=2)
    await ctx.send(f'```json\n{as_json}```')

@bot.command(description='Start submissions period')
@commands.has_role(admin_role_id)
async def submission(ctx):
    await ctx.send('Manually triggering submissions')
    data.change_period('submissions', manual_change=True)
    await submissions.submission_period()

@bot.command(description='Start voting period')
@commands.has_role(admin_role_id)
async def voting(ctx):
    await ctx.send('Manually triggering voting')
    data.change_period('voting', manual_change=True)
    await voting.voting_period()

@bot.command(description='Start results period')
@commands.has_role(admin_role_id)
async def results(ctx):
    await ctx.send('Manually triggering results')
    data.change_period('results', manual_change=True)
    await results.results_period()
