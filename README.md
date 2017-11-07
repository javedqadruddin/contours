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

The default location where you should store your data is in the package root directory in a subdirectory called data/final_data. If you unzip the data file for this Challenge in ```repo_root_directory/data/``` the data will then already be in the correct directory structure for use with this package.

If you want to set it up manually, the contour data should go in:

```repo_root_directory/data/final_data/contourfiles/```

and the image data in dicom (.dcm) file format should go in:

```repo_root_directory/data/final_data/dicoms/```

Within those directories, the actual contour files and .dcm files should be in subdirectories corresponding to each patient or study. A csv file linking the correct dicom files with the corresponding contour files should be included in:

```repo_root_directory/data/final_data/```

The csv file should have the name of the subdirectory containing the dicom for a given patient or study in the first column and the name of the subdirectory containing the contour files for that patient or study in the second column.  

Filenames should follow the same naming conventions as those provided as samples in this Challenge.

If you wish to use a different directory structure, you can do so by passing a setting object to the data generator (more on that below)

------------------

## usage

There are two main uses for this package: 
1. Run inference on directories full of dicom images and outer contour files.
2. Use a training data generator to help train a model.

Use 1: Run inference
You can run inference using a thresholding technique by doing:

```python
from contours.model import predict

predict(threshold=125, show_images=False)
```

The predict function will return a True/False mask representing the predicted inner contour. You can set show_images=True if you want to visualize the images with the predicted contour overlayed.

Use 2: Training data generator
Instantiate a TrainingDataGenerator, and use the flow_contour_data() method:

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
  'xfiles':path_to_your_image_files}
  ```

------------------


# Phase 1, Part 1 Questions

## How did you verify that you are parsing the contours correctly?
I checked the output to make sure that there were true's in the mask arrays roughly where the true's should be a for a few samples. Given more time, I would visualize the mask and superimpose that visualization on the images to verify that it looks like the contours are generally in the right place on the images themselves.  

## What changes did you make to the code, if any, in order to integrate it into our production code base?
I added a separate set of datahandler functions so that if the arrangement of the data changes (which seems a likely occurrence), only the datahandler code needs to change and the rest of the code can stay exactly the same. I also wrapped the parsing and masking functions in parser.py and preprocessor.py so that those functions can change and only their wrappers need to change rather than needing to change several things in other parts of the code.  The only change I made to the parsing.py code was to change parse_dicom_file to return the image itself rather than a dict containing the image, because, as far as I could tell, the dict wrapper served no purpose.

------------------


# Phase 1, Part 2 Questions

## Did you change anything from the pipelines built in Parts 1 to better streamline the pipeline built in Part 2? If so, what? If not, is there anything that you can imagine changing in the future?
I had looked ahead to part 2 already, so I designed everything with that in mind and didn't need to change anything at that point.

## How do you/did you verify that the pipeline was working correctly?
I checked the output to make sure that there were true's in the mask arrays roughly where the true's should be a for a few samples. Given more time, I would visualize the mask and superimpose that visualization on the images to verify that it looks like the contours are generally in the right place on the images themselves.  

## Given the pipeline you have built, can you see any deficiencies that you would change if you had more time? If not, can you think of any improvements/enhancements to the pipeline that you could build in?
- It's relatively untested given the time constraints. Given more time, I'd implement a test suite.
- I would also create a method in the TrainingDataGenerator class to be able to visualize a batch with the mask superimposed on the images for that batch. That would be helpful for the user to be able to verify that everything's working properly.
- I would implement logging to log whether any contour files were found without matching image files

# Phase 2, Part 1 Questions

## After building the pipeline, please discuss any changes that you made to the pipeline you built in Phase 1, and why you made those changes.
I updated the TrainingDataGenerator to handle being able to return just inner contours along with the image, just outer contours along with the image, or both. I anticipate that users might want to get just the inner or outer contours in some situations (like when running inference when only outer contours are available), and users might want both the inner and outer contours associated with an image (like when doing training or trying to evaluate different heuristic techniques).  That necessitated a somewhat ugly set of if statements in the generator function, but I avoided needing to make changes elsewhere. I was able to edit just one file to accomplish this because I did the best I could to make the code as modular as time permitted during Phase 1. 

# Phase 2, Part 2 Questions

## Let’s assume that you want to create a system to outline the boundary of the blood pool (i-contours), and you already know the outer border of the heart muscle (o-contours). Compare the differences in pixel intensities inside the blood pool (inside the i-contour) to those inside the heart muscle (between the i-contours and o-contours); could you use a simple thresholding scheme to automatically create the i-contours, given the o-contours? Why or why not? Show figures that help justify your answer.
First thing, I took a look at some of the images and what the inner and outer contours look like. From those images, it seemed that the pixels in the inner contours was generally lighter in color than the pixels in the outer contour that wasn't in the innner contour. The pictures looked like this:

![Alt text](./readme_images/ground_truth.png?raw=true "Ground Truth")

To test the hypothesis that there was likely a group of lighter pixels and a group of darker pixels, I made a histogram of the pixel values inside the o-contour from one of the images:

![Alt text](./readme_images/histogram.png?raw=true "Histogram")

There is a bimodal distribution here, sugesting that the hypothesis is correct. Picking a threshold between the two peaks should do a good job of predicting the inner contours. 

To test that out, I picked 155 as the threshold and visualized the results.  The predictions looked like these: 

![Alt text](./readme_images/prediction_with_outlying_islands.png?raw=true "Prediction 1")
![Alt text](./readme_images/prediction_with_islands.png?raw=true "Prediction 2")

I also visualized the pixels that were missed by the prediction:

![Alt text](./readme_images/misses.png?raw=true "Misses - False negatives")

The pixels that were marked but should not have been:

![Alt text](./readme_images/outlying_islands_only.png?raw=true "Incorrect pixels - False positives")

And the pixels that were correctly identified as inner contour pixels:

![Alt text](./readme_images/prediction_with_islands.png?raw=true "Correct pixels - True positives")

From this, I was able to evaluate precision, recall and F1 scores. For initially-chosen threshold of 155, precision and recall were in the high 90s and 80s respectively.  

To pick 155, I had simply eyeballed the histogram for a single image. It would be nice to select the threshold more systematically. So I wrote some evaluation functions with which I tried many different thresholds and averaged the precision, recall and F1 scores across the whole dataset for each threshold. 

The F1 score distribution for varying threshold values ended up looking like a parabola with a max around 125:

![Alt text](./readme_images/parabola.png?raw=true "F1 Score (y-axis) vs. Threshold (x-axis)")

I used numpy to find the best fit parabola for the datapoints, and I could have found the analytically best threshold by taking the derivative of that function and finding its maximum. 

As part of the code to test thresholds, I wrote a function to clean out faulty data that would otherwise introduce unecessary noise in the results. There were a few images like the following, where the innner and outer contours didn't entirely overlap. I think these were mistakes in labelling, so I wrote code to ignore images where that occurred:

![Alt text](./readme_images/faulty_data.png?raw=true "Faulty data?")


## Do you think that any other heuristic (non-machine learning)-based approaches, besides simple thresholding, would work in this case? Explain.

Beyond the simple thresholding I did here, I think better results could be obtained by filling in the gaps that are entirely surrounded by inner contour prediction.  For example, in this image, there are gaps within the inner contours which we know should always be inner contours:

![Alt text](./readme_images/prediction_with_islands.png?raw=true "Prediction with internal gaps")

This can be done by treating the pixels as a graph. Neighboring pixels in the prediction mask are thought of as connected if and only if they are both False (predicted to not be an inner contour pixel). You can use graph search to get all the fully connected components of the graph in the entire image.  You leave the largest fully connected component untouched (because the largest fully connected component will be the whole image lying outside the inner contour prediction), but for all smaller fully connected components, you flip all their pixels to True.  This will result in filling in the gaps within the inner contour prediction, thus increasing recall. I know this technique would work, but I did not have time to implement it.  

You can do the same thing in reverse to set disconnected islands of 'True' to 'False'.  This would serve to improve precision, though there were generally fewer of these false positives, so it wouldn't have as much of an effect as the gap elimination described above. Example: the little islands of inner contour prediction that are disconnected from the main body of inner contour in this image:

![Alt text](./readme_images/prediction_with_outlying_islands.png?raw=true "Prediction with internal gaps")



