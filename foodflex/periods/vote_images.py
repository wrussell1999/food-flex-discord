from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
from io import BytesIO
import foodflex.util.data as data
import foodflex.util.config as config


def get_submission_images():
    images = []
    letter = 'A'

    for url in data.urls:
        # GET request for Image, then opened as obj
        response = requests.get(data.urls[url])
        image = Image.open(BytesIO(response.content))

        # Make image a 256 x 256 square
        image = ImageOps.fit(image, (256, 256), Image.ANTIALIAS)

        # Add caption (letter) to image
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(
            '/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf', 32)
        draw.text((24, image.size[1] - 48), letter,
                  (255, 255, 255), font=font)

        # Compress image below 5 mb (Discord upload limit)
        image.thumbnail((256, 256), Image.ANTIALIAS)
        images.append(image)
        letter = chr(ord(letter) + 1)

        return combine_images(images)


def combine_images(images):
    all = Image.new('RGB', (256, (256 * len(images))))

    y_offset = 0
    for image in images:
        all.paste(image, (0, y_offset))
        y_offset += image.size[1]
    path = "data/all.png"
    all.save(path, optimize=True, qualty=30)
    return path
