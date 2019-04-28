import json
import logging

with open("data/config.json") as file:
    config = json.load(file)

def initilise_logging():
    logger = logging.getLogger('food-flex')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='data/foodflex.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    return logger