import logging
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
import app.data.firestore as data
logger = logging.getLogger('food-flex')

INTERNAL_RES = (1024, 1024)
OUTPUT_RES = (1024, 1024)

FONT_PATH = 'static/DejaVuSans-Bold.ttf'
FONT_BASE_SIZE = int(0.2 * INTERNAL_RES[1])
FONT_SHADOW_SIZE = int(1.125 * FONT_BASE_SIZE)

font_base = ImageFont.truetype(FONT_PATH, FONT_BASE_SIZE)
font_shadow = ImageFont.truetype(FONT_PATH, FONT_SHADOW_SIZE)


def process_image(url, letter):
    logger.debug(f'Download & process {url}')

    image_loaded = False
    try:
        response = requests.get(url, timeout=5)
        try:
            response.raise_for_status()
            try:
                image = Image.open(BytesIO(response.content))
                image = rotate_if_exif_specifies(image)
                image_loaded = True
            except OSError:
                logger.error('Image decoding error')

        except requests.HTTPError:
            logger.error('HTTP error')

    except requests.exceptions.ConnectionError:
        logger.error('Network error')

    # Replace image with a grey background if it does not load
    if not image_loaded:
        image = Image.new('RGB', (1, 1), color='grey')

    # Scale image to fixed size
    image = ImageOps.fit(image, INTERNAL_RES, method=Image.ANTIALIAS)
    draw = ImageDraw.Draw(image)

    # Draw 'error' if image could not be loaded
    if not image_loaded:
        pos = (INTERNAL_RES[0] * 0.19, INTERNAL_RES[1] * 0.35)
        draw.text(pos, 'error', font=font_shadow, fill='black')

    # Add letter to corner of image
    x, y = (INTERNAL_RES[0] * 0.05, INTERNAL_RES[1] * 0.01)
    draw.text((x, y), letter, font=font_shadow, fill='black')
    draw.text((x-1, y-1), letter, font=font_base, fill='white')

    # Resize image if needed
    if INTERNAL_RES != OUTPUT_RES:
        image = image.resize(OUTPUT_RES, Image.NEAREST)

    buffer = BytesIO()
    image.save(buffer, format='png', compress_level=6)

    logger.debug(f'Done, {buffer.tell() // 1024} KB image created ')
    buffer.seek(0)
    return buffer


def rotate_if_exif_specifies(image):
    try:
        exif_tags = image._getexif()
        if exif_tags is None:
            # No EXIF tags, so we don't need to rotate
            logger.debug('No EXIF data, so not transforming')
            return image

        value = exif_tags[274]
    except KeyError:
        # No rotation tag present, so we don't need to rotate
        logger.debug('EXIF data present but no rotation tag, so not transforming')
        return image

    value_to_transform = {
        1: (0, False),
        2: (0, True),
        3: (180, False),
        4: (180, True),
        5: (-90, True),
        6: (-90, False),
        7: (90, True),
        8: (90, False)
    }

    try:
        angle, flip = value_to_transform[value]
    except KeyError:
        logger.warn(f'EXIF rotation \'{value}\' unknown, not transforming')
        return image

    logger.debug(f'EXIF rotation \'{value}\' detected, rotating {angle} degrees, flip: {flip}')
    if angle != 0:
        image = image.rotate(angle)

    if flip:
        image = image.tranpose(Image.FLIP_LEFT_RIGHT)

    return image
