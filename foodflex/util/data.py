import json
from . import config

with open("data/quotes.json") as quote_file:
    quotes = json.load(quote_file)

with open("data/leaderboard.json") as score_file:
    leaderboard_data = json.load(score_file)

with open("data/data.json") as temp_file:
    daily_data = json.load(temp_file)

with open("data/strings.json") as strings_file:
    strings = json.load(strings_file)

logger = config.initilise_logging()


def save_data():
    logger.debug("Daily data saved")
    with open('data/data.json', 'w') as json_file:
        json.dump(daily_data, json_file)


def save_leaderboard():
    logger.debug("Leaderboard data saved")
    with open('data/leaderboard.json', 'w') as json_file:
        json.dump(leaderboard_data, json_file)
