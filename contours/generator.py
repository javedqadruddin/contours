from numpy.random import shuffle
from numpy import array as np_array
from numpy import append as np_append


from contours.preprocessors import preprocessor
from contours.handlers import datahandler

class TrainingDataGenerator(object):
    def __init__(self, settings=None):
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
        if not settings:
            self.file_list = datahandler.get_file_list()
        else:
            self.file_list = datahandler.get_file_list(settings)

    def flow_contour_data(self, batch_size=8):
        """Returns generator that perpetually yields batches, randomizing
        the order of training examples each epoch

        :param batch_size: size of desired batch
        :return: generator that yields batches of size batch_size infinitely
        """
        while True:
            # randomizes the order of the data
            file_list = self.file_list
            shuffle(file_list)
            current_batch_img = []
            current_batch_target = []
            # when the for loop completes its iteration, that is one epoch
            for file_pair in file_list:
                img, target = preprocessor.preprocess(file_pair)
                current_batch_img.append(img)
                current_batch_target.append(target)
                if len(current_batch_img) == batch_size:
                    yield (np_array(current_batch_img),
                            np_array(current_batch_target))
                    # flush the arrays when batch is complete
                    current_batch_img = np_array([])
                    current_batch_target = np_array([])
