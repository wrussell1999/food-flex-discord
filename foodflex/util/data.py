import json
from . import config

with open('data/quotes.json') as quote_file:
    quotes = json.load(quote_file)

with open('data/leaderboard.json') as score_file:
    leaderboard_data = json.load(score_file)

with open('data/data.json') as temp_file:
    content = json.load(temp_file)
    try:
        daily_data = content['daily_data']
        letter_to_user_id = content['letter_to_user_id']
    except KeyError:
        daily_data = {}
        letter_to_user_id = {}

with open('data/strings.json') as strings_file:
    strings = json.load(strings_file)

with open('data/shared_prefs.json') as sp_file:
    shared_prefs = json.load(sp_file)

logger = config.initilise_logging()


def save_data():
    with open('data/data.json', 'w') as json_file:
        json.dump({
            'daily_data': daily_data,
            'letter_to_user_id': letter_to_user_id
        }, json_file)

    logger.debug('Daily data saved')


def save_leaderboard():
    logger.debug('Leaderboard data saved')
    with open('data/leaderboard.json', 'w') as json_file:
        json.dump(leaderboard_data, json_file)


def save_prefs():
    with open('data/shared_prefs.json', 'w') as json_file:
        json.dump(shared_prefs, json_file)
