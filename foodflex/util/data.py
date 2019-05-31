import json
from . import config

with open("data/quotes.json") as quote_file:
    quotes = json.load(quote_file)

with open("data/scoreboard.json") as score_file:
    overall_score = json.load(score_file)

with open("data/daily_data.json") as temp_file:
    daily_data = json.load(temp_file)

logger = config.initilise_logging()

def score_dict_to_json():
    logger.debug("'scoreboard' dumped to scoreboard.json")
    with open('data/scoreboard.json', 'w') as json_file:
        json.dump(overall_score, json_file)

def data_dict_to_json():
    logger.debug("'data' dumped to daily_data.json")
    with open('data/daily_data.json', 'w') as json_file:
        json.dump(daily_data, json_file)