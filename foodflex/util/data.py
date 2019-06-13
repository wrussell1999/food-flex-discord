import json
import logging
from . import config
logger = logging.getLogger('food-flex')


logger.debug('Loading quotes...')
with open('data/quotes.json') as file:
    quotes = json.load(file)

logger.debug('Loading leaderboard...')
with open('data/leaderboard.json') as file:
    leaderboard_data = json.load(file)

logger.debug('Loading daily data...')
with open('data/data.json') as file:
    content = json.load(file)
    try:
        daily_data = content['daily_data']
        letter_to_user_id = content['letter_to_user_id']
        logger.debug("Existing entries in daily data, restoring from file")
    except KeyError:
        daily_data = {}
        letter_to_user_id = {}
        logger.debug("No entries in daily data, creating blank template")

logger.debug('Loading strings...')
with open('data/strings.json') as strings_file:
    strings = json.load(strings_file)

logger.debug('Loading shared prefs...')
with open('data/shared_prefs.json') as sp_file:
    shared_prefs = json.load(sp_file)


def save_data():
    logger.debug('Saving daily data...')
    with open('data/data.json', 'w') as file:
        json.dump({
            'daily_data': daily_data,
            'letter_to_user_id': letter_to_user_id
        }, file)


def save_leaderboard():
    logger.debug('Saving leaderboard...')
    with open('data/leaderboard.json', 'w') as file:
        json.dump(leaderboard_data, file)


def save_prefs():
    logger.debug('Saving shared prefs...')
    with open('data/shared_prefs.json', 'w') as file:
        json.dump(shared_prefs, file)
