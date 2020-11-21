from PIL import Image
import io


def make_square(im, min_size=256, fill_color=(255, 255, 255, 1)):
    im = Image.open(im)
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im
