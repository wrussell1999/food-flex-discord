import sys
import json

from foodflex.util.logging import logger

CONFIG_PATH = 'config/config.json'


def load():
    global token, server_id, admin_ids, main_channel_id, leaderboard_channel_id
    logger.info('Loading config...')
    try:
        with open(CONFIG_PATH) as file:
            try:
                config = json.load(file)
            except json.decoder.JSONDecodeError:
                fatal(f'↳ Cannot parse {CONFIG_PATH}')

            try:
                token = config['token']
                server_id = config['server_id']
                admin_ids = config['admin_ids']
                main_channel_id = config['main_channel_id']
                leaderboard_channel_id = config['leaderboard_channel_id']
                logger.debug('↳ Config loaded')
            except KeyError:
                fatal(f'↳ Cannot find required keys in {CONFIG_PATH}\
                      \nSee README.md for required structure')
    except OSError:
        fatal(f'↳ Cannot open {CONFIG_PATH}')


def fatal(message):
    logger.critical(message)
    sys.exit(1)
