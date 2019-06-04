import json
import logging

with open("config/config.json") as file:
    config = json.load(file)


def initilise_logging():
    logging.basicConfig(level=logging.INFO) # discord.py
    logger = logging.getLogger('food-flex')  # food-flex
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='data/foodflex.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    return logger
