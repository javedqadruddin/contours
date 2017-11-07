from numpy import array as np_array

def contained_in(inner_mask, outer_mask):
    inner_pixels = get_pixel_positions(inner_mask)
    outer_pixel_set = set(get_pixel_positions(outer_mask))
    for pixel in inner_pixels:
        if pixel not in outer_pixel_set:
            return False
    return True

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
