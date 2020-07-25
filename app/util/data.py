import os
import sys
import json

from foodflex.util.logging import logger

DEFAULT_PERIOD = 'submissions'
DEFAULT_MODE = 'automatic'

DATA_PATH = 'data'
STATE_PATH = f'{DATA_PATH}/state.json'
LEADERBOARD_PATH = f'{DATA_PATH}/leaderboard.json'


def change_period(new_period, manual_change=False):
    global period, mode

    if manual_change:
        mode = 'manual'
    else:
        mode = 'automatic'

    logger.info(f'Period \'{period}\' -> \'{new_period}\' ({mode})')

    period = new_period
    save_state()


def set_mode(new_mode):
    global mode

    logger.info(f'Mode \'{mode}\' -> \'{new_mode}\'')
    mode = new_mode
    save_state()

def set_paths(data_path: str):
    DATA_PATH = data_path
    STATE_PATH = f'{DATA_PATH}/state.json'
    LEADERBOARD_PATH = f'{DATA_PATH}/leaderboard.json'


def load_state():
    global participants, voting_map, period, mode

    logger.debug('Loading state...')
    try:
        with open(STATE_PATH, 'r') as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                fatal(f'↳ Cannot parse {STATE_PATH}')
            try:
                participants = data['participants']
                voting_map = data['voting_map']
                period = data['period']
                mode = data['mode']
                logger.info('↳ Using existing state file')
            except KeyError:
                fatal(f'↳ Cannot find required keys in {STATE_PATH}')
    except OSError:
        participants = {}
        voting_map = {}
        period = DEFAULT_PERIOD
        mode = DEFAULT_MODE
        logger.info('↳ No existing state file, starting with blank state')
        save_state()


def load_leaderboard():
    global leaderboard, leaderboard_message_id

    logger.debug('Loading leaderboard...')
    try:
        with open(LEADERBOARD_PATH) as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                fatal(f'↳ Cannot parse {LEADERBOARD_PATH}')
            try:
                leaderboard = data['leaderboard']
                leaderboard_message_id = data['leaderboard_message_id']
                logger.info('↳ Using existing leaderboard file')
            except KeyError:
                fatal(f'↳ Cannot find required keys in {LEADERBOARD_PATH}')
    except OSError:
        leaderboard = {}
        leaderboard_message_id = None
        logger.info('↳ No existing leaderboard file, starting with blank')
        save_leaderboard()


def save_state():
    global participants, voting_map, period, mode

    logger.debug('Saving state...')

    try:
        os.makedirs(DATA_PATH, exist_ok=True)
        with open(STATE_PATH, 'w') as file:
            json.dump({
                'participants': participants,
                'voting_map': voting_map,
                'period': period,
                'mode': mode
                }, file, indent=2)
            logger.info('State saved')
    except OSError:
        fatal(f'↳ Could not save to {STATE_PATH}')


def save_leaderboard():
    global leaderboard, leaderboard_message_id

    logger.debug('Saving leaderboard...')
    try:
        os.makedirs(DATA_PATH, exist_ok=True)
        with open(LEADERBOARD_PATH, 'w') as file:
            json.dump({
                'leaderboard': leaderboard,
                'leaderboard_message_id': leaderboard_message_id
                }, file, indent=2)
            logger.info('Leaderboard saved')
    except OSError:
        fatal(f'↳ Could not save to {STATE_PATH}')


def fatal(message):
    logger.critical(message)
    sys.exit(1)
