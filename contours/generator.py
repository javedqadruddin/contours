from numpy.random import shuffle
from numpy import array as np_array
from numpy import append as np_append
from os import path

from contours.preprocessors import preprocessor
from contours.handlers import datahandler

HERE = path.abspath(path.dirname(__file__))
#CONTOURS_DIR = path.dirname(HERE)
PACKAGE_DIR = path.dirname(HERE)
DATA_DIR = path.join(PACKAGE_DIR, 'data/final_data')
CONTOURFILES_DIR = path.join(DATA_DIR, 'contourfiles')
IMGFILES_DIR = path.join(DATA_DIR, 'dicoms')
INNER_CONTOUR_DIRNAME = 'i-contours'
OUTER_CONTOUR_DIRNAME = 'o-contours'

SETTINGS = {'csv':path.join(DATA_DIR,'link.csv'),
            'yfiles':CONTOURFILES_DIR,
            'xfiles':IMGFILES_DIR,
            'contour_type':'i-contours'}


class TrainingDataGenerator(object):
    def __init__(self, contour_option='both', settings=SETTINGS):
        """Object to wrap a generator that infinitely yields batches of training
        data.

        :param settings: if data is not in the default location, pass a settings
        object of the following format:
        {'csv':~path to your csv file linking image files and contour files~,
                    'yfiles':~path to your contour files~,
                    'xfiles':~path to your image files~,
                    'contour_type':~either 'i-contours' for inner contours or
                    'o-contours' for outer contours}
        """
        self.settings = settings
        if contour_option == 'inner':
            settings['contour_type'] = INNER_CONTOUR_DIRNAME
            self.file_list = datahandler.get_file_list(settings)
        elif contour_option == 'outer':
            settings['contour_type'] = OUTER_CONTOUR_DIRNAME
            self.file_list = datahandler.get_file_list(settings)
        else:
            settings['contour_type'] = INNER_CONTOUR_DIRNAME
            inner_file_list = datahandler.get_file_list(settings)
            settings['contour_type'] = OUTER_CONTOUR_DIRNAME
            outer_file_list = datahandler.get_file_list(settings)
            self.file_list = self._normalize_file_lists(inner_file_list, outer_file_list)


    def _normalize_file_lists(self, inner_list, outer_list):
        set1 = set([i for i,j in inner_list])
        set2 = set([i for i,j in outer_list])
        images_not_in_set1 = set2 - set1
        common_images = set2 - images_not_in_set1

        common_files_inner = [i for i in inner_list if i[0] in common_images]
        common_files_outer = {i:j for i,j in outer_list if i in common_images}

        output = []
        for img_file, inner_cont_file in common_files_inner:
            if img_file in common_files_outer:
                output.append((img_file, inner_cont_file, common_files_outer[img_file]))
        return output

    def flow_contour_data(self, batch_size=8):
        """Returns generator that perpetually yields batches, randomizing
        the order of training examples each epoch

        :param batch_size: size of desired batch
        :return: generator that yields batches of size batch_size infinitely
        """
        current_batch_img = []
        current_batch_target = []
        current_batch_outer = []
        while True:
            # randomizes the order of the data
            file_list = self.file_list
            shuffle(file_list)

            # when the for loop completes its iteration, that is one epoch
            for file_set in file_list:
                if len(file_set) == 2:
                    img, target = preprocessor.preprocess(file_set)
                    current_batch_img.append(img)
                    current_batch_target.append(target)
                else:
                    file_pair = (file_set[0], file_set[1])
                    img, inner_target = preprocessor.preprocess(file_pair)
                    file_pair = (file_set[0], file_set[2])
                    img, outer_contour = preprocessor.preprocess(file_pair)
                    current_batch_img.append(img)
                    current_batch_target.append(inner_target)
                    current_batch_outer.append(outer_contour)
                if len(current_batch_img) == batch_size:
                    if len(file_set) == 2:
                        yield (np_array(current_batch_img),
                                np_array(current_batch_target))
                    else:
                        yield (np_array(current_batch_img),
                                np_array(current_batch_target),
                                np_array(current_batch_outer))
                    # flush the arrays when batch is complete
                    current_batch_img = []
                    current_batch_target = []
                    current_batch_outer = []
