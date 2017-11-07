from numpy import array as np_array


def to_mask(image, pixels):
    mask = empty_mask(image.shape)
    for pixel in pixels:
        x,y = pixel
        mask[x][y] = True
    return mask

def empty_mask(shape):
    width, height = shape
    empty_mask = np_array([[False] * height] * width)
    return empty_mask
