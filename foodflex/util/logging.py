import sys
import logging

def init():
    global logger
    logging.addLevelName(logging.WARNING, 'WARN')
    logger = logging.getLogger('food-flex')
    logger.setLevel(logging.DEBUG)

    console_format = logging.Formatter('%(asctime)s %(levelname)5s %(module)11s: %(message)s'
                                       , '%H:%M:%S')
    file_format = logging.Formatter('%(asctime)s %(levelname)5s %(module)11s: %(message)s'
                                    , '%d/%m/%y %H:%M:%S')

    file_handler = logging.FileHandler(filename='foodflex.log', encoding='utf-8', mode='w')
    file_handler.setFormatter(file_format)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_format)
    console_handler.setLevel(logging.DEBUG)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
