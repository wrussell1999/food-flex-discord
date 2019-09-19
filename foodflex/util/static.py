import sys
import json

from foodflex.util.logging import logger

QUOTES_PATH = 'static/quotes.json'
STRINGS_PATH = 'static/strings.json'


def load():
    global quotes, strings
    logger.info('Loading quotes & strings...')
    try:
        with open(QUOTES_PATH) as file:
            try:
                quotes = json.load(file)
            except json.decoder.JSONDecodeError:
                fatal(f'↳ Cannot parse {QUOTES_PATH}')
    except OSError:
        fatal(f'↳ Cannot open {QUOTES_PATH}')

    try:
        with open(STRINGS_PATH) as file:
            try:
                strings = json.load(file)
            except json.decoder.JSONDecodeError:
                fatal(f'↳ Cannot parse {STRINGS_PATH}')
    except OSError:
        fatal(f'↳ Cannot open {STRINGS_PATH}')

    logger.debug('↳ Quotes & strings loaded')

def fatal(message):
    logger.critical(message)
    sys.exit(1)
