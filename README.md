# contours

------------------

## purpose

This package can be used to generate training data for image segmentation models from dicom medical image files and contour maps of the x,y coordinates of objects of interest in the images.

------------------

## setup

Prior to setting up the package, you may want to set up a virtual environment for it to run in. You can do that by following the instructions [here](https://virtualenv.pypa.io/en/stable/)

To set up the package, simply clone this repo, navigate to the root directory of the repo (the directory that contains the file setup.py) and type the following shell command:
```
pip install -e .
```

The default location where you should store your data is in the package root directory in a subdirectory called data/final_data

If you wish to use a different directory, you can do so by passing a setting object to the data generator (more on that below)

------------------

## usage

To use the package, simply import it in the python script of your choice, instantiate a TrainingDataGenerator, and use the flow_contour_data() method:

```python
from contours.generator import TrainingDataGenerator

my_batch_size = 8
my_generator = TrainingDataGenerator()
gen = TrainingDataGenerator.flow_contour_data(my_batch_size)
```

You can then call ```next(gen)``` to get a batch of data. Or, you can pass the generator gen as a parameter to a method like keras.model.fit_generator().  See [here](https://keras.io/models/model/) for that usage.

If your data is somewhere other than the default location mentioned above, pass TrainingDataGenerator a settings object when you instantiate it.  The settings object should be a dict of the following format:
```python
{'csv':path_to_your_csv_file_that_links_contour_and_image_files,
  'yfiles':path_to_your_contour_files,
  'xfiles':path_to_your_image_files,
  'contour_type':name_of_type_of_contours_you_are_using_eg_i-contours_or_o-contours}
  ```

------------------


# Part 1 Questions

## How did you verify that you are parsing the contours correctly?
I checked the output to make sure that there were true's in the mask arrays roughly where the true's should be a for a few samples. Given more time, I would visualize the mask and superimpose that visualization on the images to verify that it looks like the contours are generally in the right place on the images themselves.  

## What changes did you make to the code, if any, in order to integrate it into our production code base?
I added a separate set of datahandler functions so that if the arrangement of the data changes (which seems a likely occurrence), only the datahandler code needs to change and the rest of the code can stay exactly the same. I also wrapped the parsing and masking functions in parser.py and preprocessor.py so that those functions can change and only their wrappers need to change rather than needing to change several things in other parts of the code.  The only change I made to the parsing.py code was to change parse_dicom_file to return the image itself rather than a dict containing the image, because, as far as I could tell, the dict wrapper served no purpose.

------------------


# Part 2 Questions

## Did you change anything from the pipelines built in Parts 1 to better streamline the pipeline built in Part 2? If so, what? If not, is there anything that you can imagine changing in the future?
I had looked ahead to part 2 already, so I designed everything with that in mind and didn't need to change anything at that point.

## How do you/did you verify that the pipeline was working correctly?
I checked the output to make sure that there were true's in the mask arrays roughly where the true's should be a for a few samples. Given more time, I would visualize the mask and superimpose that visualization on the images to verify that it looks like the contours are generally in the right place on the images themselves.  

## Given the pipeline you have built, can you see any deficiencies that you would change if you had more time? If not, can you think of any improvements/enhancements to the pipeline that you could build in?
- It's relatively untested given the time constraints. Given more time, I'd implement a test suite.
- I would also create a method in the TrainingDataGenerator class to be able to visualize a batch with the mask superimposed on the images for that batch. That would be helpful for the user to be able to verify that everything's working properly.
- I would implement logging to log whether any contour files were found without matching image files
