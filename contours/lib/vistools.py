import matplotlib.pyplot as plt

from contours.lib import utils


def show_training_data(image, inner_mask, outer_mask):
    img1 = plt.imshow(image, cmap='gray')
    img2 = plt.imshow(inner_mask, cmap=plt.cm.viridis, alpha=.2)
    img3 = plt.imshow(outer_mask, cmap=plt.cm.PuRd, alpha=.2)
    plt.show()


def show_prediction(image, predict_mask):
    img1 = plt.imshow(image, cmap='gray')
    img2 = plt.imshow(predict_mask, cmap=plt.cm.viridis, alpha=.2)
    plt.show()


def show_pixels(image, pixels):
    pixel_mask = utils.to_mask(image, pixels)
    img1 = plt.imshow(image, cmap='gray')
    img2 = plt.imshow(pixel_mask, cmap=plt.cm.viridis, alpha=.2)
    plt.show()


def visualize(image, inner_mask, outer_mask, predict_mask, correct_pixels, missed_pixels, incorrect_pixels):
    show_training_data(image, inner_mask, outer_mask)
    show_prediction(image, predict_mask)
    show_pixels(image, correct_pixels)
    show_pixels(image, missed_pixels)
    show_pixels(image, incorrect_pixels)
