import sys
import json
import os
from environs import Env
from foodflex.util.logging import logger

CONFIG_PATH = 'config/config.json'


def load():
    global token, server_id, command_prefix, admin_ids, main_channel_id, leaderboard_channel_id, data_root
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
                command_prefix = config['command_prefix']
                admin_ids = config['admin_ids']
                main_channel_id = config['main_channel_id']
                leaderboard_channel_id = config['leaderboard_channel_id']
                data_root = config['data_root']
                logger.debug('↳ Config loaded')
            except KeyError:
                fatal(f'↳ Cannot find required keys in {CONFIG_PATH}\
                      \nSee README.md for required structure')
    except OSError:
        logger.warn(f'↳ Cannot open {CONFIG_PATH}')
        env = Env()
        token = env('TOKEN')
        server_id = env.int('SERVER_ID')
        command_prefix = env('COMMAND_PREFIX')
        admin_ids = list(map(lambda x: int(x), env.list('ADMIN_IDS')))
        main_channel_id = env.int('MAIN_CHANNEL_ID')
        leaderboard_channel_id = env.int('LEADERBOARD_CHANNEL_ID')
        data_root = env('DATA_ROOT')
        logger.debug('↳ Config loaded from environment')



def fatal(message):
    logger.critical(message)
    sys.exit(1)
