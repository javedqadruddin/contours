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


def get_directories(settings):
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


def get_img_filename(contour_filename):
    prefix_removed = contour_filename.replace(CONTOUR_FILENAME_PREFIX, '')
    suffix_removed = prefix_removed.split('-')[0]
    preceding_zeros_removed = suffix_removed.lstrip('0')
    return preceding_zeros_removed + IMG_FILE_EXTENSION


def get_files(x_dir, y_dir):
    filepaths = []
    img_filenames = listdir(x_dir)
    for contour_filename in listdir(y_dir):
        corresponding_img_filename = get_img_filename(contour_filename)
        if corresponding_img_filename in img_filenames:
            img_path = path.join(x_dir, corresponding_img_filename)
            contour_path = path.join(y_dir, contour_filename)
            filepaths.append((img_path, contour_path))
    return filepaths


def get_file_list(settings=SETTINGS):
    data_directories = get_directories(settings)
    file_list = []
    for x_dir, y_dir in data_directories:
        for img_file, contour_file in get_files(x_dir, y_dir):
            file_list.append((img_file, contour_file))
    return file_list

def main():
    get_file_list()

if __name__ == "__main__":
    main()
