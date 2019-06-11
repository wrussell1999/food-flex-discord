from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import requests
from io import BytesIO
import foodflex.util.data as data
import foodflex.util.config as config

def get_submission_images():
    images = []
    letter = 'A'
    
    for url in data.daily_data'[urls']:
        response = requests.get(url[1])
        caption = url[0] + ", " + letter
        letter = chr(ord(letter) + 1_

