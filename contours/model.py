import contours
from contours.lib import utils

def get_pixel_positions(mask):
    # given a mask, gives you the pixel positions of the pixels marked True in the mask
    contour_pixels = []
    for x, row in enumerate(mask):
        for y, col_val in enumerate(row):
            if col_val == True:
                contour_pixels.append((x,y))
    return contour_pixels


def predict_inner(image, outer_pixels, threshold):
    predict_mask = utils.empty_mask(image.shape)
    for pixel in outer_pixels:
        x,y = pixel
        pixel_val = image[x][y]
        if pixel_val >= threshold:
            predict_mask[x][y] = True
    return predict_mask


def predict(settings=None, threshold=125, show_images=False):
    # settings allows user to input directories to look in for the image files
    # and contour files. If settings not entered, will look in default location
    # see README.md for format and usage of settings 
    if settings:
        outer_generator = contours.generator.TrainingDataGenerator(contour_option='outer', settings=settings)
    else:
        outer_generator = contours.generator.TrainingDataGenerator(contour_option='outer')
    o_gen = outer_generator.flow_contour_data(epoch_msg=True)
    batch = next(o_gen)
    preds = []
    while batch != 'end epoch':
        images, outer_masks = batch
        for image, mask in zip(images, outer_masks):
            outer_pixels = get_pixel_positions(mask)
            preds.append(predict_inner(image, outer_pixels, threshold))
            if show_images:
                contours.lib.vistools.show_prediction(image, mask)
        batch = next(o_gen)
    return preds
