"""Code that gets filenames for the datafiles and returns
an array of the filenames in x,y (input, target) pairs"""

from os import path, listdir
import csv

HERE = path.abspath(path.dirname(__file__))
CONTOURS_DIR = path.dirname(HERE)
PACKAGE_DIR = path.dirname(CONTOURS_DIR)
DATA_DIR = path.join(PACKAGE_DIR, 'data/final_data')
CONTOURFILES_DIR = path.join(DATA_DIR, 'contourfiles')
IMGFILES_DIR = path.join(DATA_DIR, 'dicoms')

CONTOUR_FILENAME_PREFIX = 'IM-0001-'
IMG_FILE_EXTENSION = '.dcm'

SETTINGS = {'csv':path.join(DATA_DIR,'link.csv'),
            'yfiles':CONTOURFILES_DIR,
            'xfiles':IMGFILES_DIR,
            'contour_type':'i-contours'}


def _get_directories(settings):
    """Gets the names of the directories containing the training data files
    from the csv that contains them and returns as a list of tuples for the
    directory containing input data (images) and directory containing
    corresponding y data (contour info)
    """
    csv_path = path.abspath(settings['csv'])
    x_base_directory_path = path.abspath(settings['xfiles'])
    y_base_directory_path = path.abspath(settings['yfiles'])

    reader = csv.DictReader(open(csv_path))
    # fieldnames are the names of the columns in the csv
    fieldnames = reader.fieldnames
    directory_names = [(row[fieldnames[0]],row[fieldnames[1]]) for row in reader]

    directory_paths = []
    for x_dir_name, y_dir_name in directory_names:
        x_directory = path.join(x_base_directory_path, x_dir_name)
        y_directory = path.join(y_base_directory_path, y_dir_name)
        y_directory = path.join(y_directory, settings['contour_type'])
        directory_paths.append((x_directory, y_directory))

    return directory_paths


def _get_img_filename(contour_filename):
    """ mapping contour filename to the corresponding image filename """
    prefix_removed = contour_filename.replace(CONTOUR_FILENAME_PREFIX, '')
    suffix_removed = prefix_removed.split('-')[0]
    preceding_zeros_removed = suffix_removed.lstrip('0')
    return preceding_zeros_removed + IMG_FILE_EXTENSION


def _get_files(x_dir, y_dir):
    """Get paths to corresponding DICOM file contour file pairs

    :param x_dir: filepath to a directory containing DICOM files
    :param y_dir: filepath to a directory containing contour files
    :return: list of tuples of paths to corresponding DICOM file, contour file
    pairs
    """
    filepaths = []
    img_filenames = listdir(x_dir)

    for contour_filename in listdir(y_dir):
        corresponding_img_filename = _get_img_filename(contour_filename)
        # if there is no corresponding image file, ignore this contour file
        if corresponding_img_filename in img_filenames:
            img_path = path.join(x_dir, corresponding_img_filename)
            contour_path = path.join(y_dir, contour_filename)
            filepaths.append((img_path, contour_path))

    return filepaths


def get_file_list(settings=SETTINGS):
    """Get list of paths to all training data files in image,target pairs

    :param settings: if the data are not in the default folder described in
    README.md, pass this method a settings object in the following format:
    {'csv':~path to your csv file linking image files and contour files~,
                'yfiles':~path to your contour files~,
                'xfiles':~path to your image files~,
                'contour_type':~either 'i-contours' for inner contours or
                'o-contours' for outer contours}
    :return: list of tuples of paths to corresponding DICOM file, contour file
    pairs
    """
    data_directories = _get_directories(settings)
    file_list = []
    for x_dir, y_dir in data_directories:
        for img_file, contour_file in _get_files(x_dir, y_dir):
            file_list.append((img_file, contour_file))
    return file_list


def main():
    """ this script can be run from command line for testing purposes"""
    print(get_file_list())

if __name__ == "__main__":
    main()
