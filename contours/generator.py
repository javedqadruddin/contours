from numpy.random import shuffle
from numpy import array as np_array
from numpy import append as np_append


from contours.preprocessors import preprocessor
from contours.handlers import datahandler

class TrainingDataGenerator(object):
    def __init__(self, settings=None):
        if not settings:
            self.file_list = datahandler.get_file_list()
        else:
            self.file_list = datahandler.get_file_list(settings)

    def flow_contour_data(self, batch_size=8):
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


def main():
    gen = TrainingDataGenerator()
    print(next(gen.flow_contour_data())[1][4][0])

if __name__ == "__main__":
    main()
