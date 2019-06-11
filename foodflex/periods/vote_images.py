from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import foodflex.util.data as data
import foodflex.util.config as config


def get_submission_images():
    images = []
    letter = 'A'

    for url in data.daily_data['urls']:
        response = requests.get(url[1])

        image = Image.open(BytesIO(response.content))
        image = ImageOps.fit(image, (256, 256), Image.ANTIALIAS)  # Make square

        # Caption -> Name and Letter
        caption = url[0] + ", " + letter
        letter = chr(ord(letter) + 1)

        # Add caption to image
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(
            '/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf', 32)
        draw.text((24, image.size[1] - 48), caption,
                  (255, 255, 255), font=font)
        image.thumbnail((256, 256), Image.ANTIALIAS)  # Compress
        images.append(image)

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
