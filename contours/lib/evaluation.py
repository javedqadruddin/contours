""" Tools for evaluating different thresholds
You can find these functions and examples of their uses in Experiments.ipynb
"""

from contours.lib import utils
from contours import model

def get_pixel_positions(mask):
    # given a mask, gives you the pixel positions of the pixels marked True in the mask
    contour_pixels = []
    for x, row in enumerate(mask):
        for y, col_val in enumerate(row):
            if col_val == True:
                contour_pixels.append((x,y))
    return contour_pixels


def get_incorrect_pixels(predict_mask, inner_mask):
    predicted_pixels = get_pixel_positions(predict_mask)
    incorrect_pixels = []
    for pixel in predicted_pixels:
        x,y = pixel
        if inner_mask[x][y]==False:
            incorrect_pixels.append((x,y))
    return incorrect_pixels


def get_correct_and_missed_pixels(predict_mask, inner_mask):
    correct_pixels = []
    missed_pixels = []
    target_pixels = get_pixel_positions(inner_mask)
    for pixel in target_pixels:
        x,y = pixel
        if predict_mask[x][y]==True:
            correct_pixels.append((x,y))
        else:
            missed_pixels.append((x,y))
    return correct_pixels, missed_pixels


def get_precision_recall(correct_pixels, missed_pixels, incorrect_pixels):
    true_positives = float(len(correct_pixels))
    false_positives = float(len(incorrect_pixels))
    false_negatives = float(len(missed_pixels))
    try:
        precision = true_positives / (true_positives + false_positives)
    except ZeroDivisionError:
        precision = 0
    try:
        recall = true_positives / (true_positives + false_negatives)
    except ZeroDivisionError:
        recall = 0
    return precision, recall


def evaluate_batch(batch, threshold, show_images=False, clean_data=False):
    metrics = []
    images, inner_masks, outer_masks = batch
    for image, inner_mask, outer_mask in zip(images, inner_masks, outer_masks):
        if clean_data and not utils.contained_in(inner_mask, outer_mask):
            continue
        outer_pixels = get_pixel_positions(outer_mask)
        predict_mask = model.predict_inner(image, outer_pixels, threshold)
        correct_pixels, missed_pixels = get_correct_and_missed_pixels(predict_mask, inner_mask)
        incorrect_pixels = get_incorrect_pixels(predict_mask, inner_mask)
        metrics.append(get_precision_recall(correct_pixels, missed_pixels, incorrect_pixels))
        if show_images:
            visualize(image, inner_mask, outer_mask, predict_mask, correct_pixels, missed_pixels, incorrect_pixels)
    return metrics


def evaluate_epoch(threshold, show_images=False, clean_data=False):
    data_generator = contours.generator.TrainingDataGenerator(contour_option='both')
    data_gen = data_generator.flow_contour_data(epoch_msg=True)
    batch = next(data_gen)
    metrics = []
    while batch != 'end epoch':
        metrics.append(evaluate_batch(batch, threshold, show_images=show_images, clean_data=clean_data))
        batch = next(data_gen)
    return metrics
