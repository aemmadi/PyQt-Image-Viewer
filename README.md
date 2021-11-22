# PyQT-Image-Viewer

Image viewer built with python and the Qt5 framework

<img width="1105" alt="Screen Shot 2021-11-22 at 4 27 44 PM" src="https://user-images.githubusercontent.com/33047045/142941850-9657eb87-e41e-40fb-bb54-bc6fbf059912.png">


## Features

- Open `jpg` images using `Ctrl + O` or `File menu -> Open`
- Move around image using trackpad or mouse with scroll bars
- **Zoom**:
  - Zoom in using `Ctrl + +` or `View Menu -> Zoom In`
  - Zoom out using `Ctrl + -` or `View Menu -> Zoom Out`
  - Reset Zoom using `Ctrl + R` or `View Menu -> Reset Zoom`
- **Edit Image Contrast**:
  - Once image is loaded in, use `Ctrl + F` or `View Menu -> Edit Image Contrast` (Opens new small window with slider)
  - Move slider around to view changes
- **Save Image**:
  - Once image is edited, use `Ctrl + S` or `File Menu -> Save Image` to save image
  - Image will be saved in the directory of where the project is being run

## Technical Implementation

- Utilized Python `PyQt5` framework to run a native desktop application
- Opens file as a `QImage` and converts it to a `QPixMap` to render as a `QLabel` on application the user interacts with
- Zoom features are implemented using the `scale` and `resize` properties of `QLabel`
  - Scales image with a factor of +/- 25%
  - Reset zoom option just sets the resize back to original image size
- Contrast feature is implemented using the `PIL`/`Pillow` library to modify contrast levels
  - When image is opened, a image buffer is created before the `QImage` is converted to `QPixMap`
  - This buffer is loaded into `PIL` for modification
  - Meanwhile, a second window `ContrastView` is rendered on the screen with a simple slider (`QSlider`) that sets contrast levels
  - There is a `onValueChanged` property for the `QSlider` that is used to update the count value next to the slider and also used to pass the value into the `ImageEnhancer` from `PIL` for contrast level modifications
  - Once `PIL` modifies the image, the image needs to be converted back from `PIL` into a `QImage` to reset the `QPixMap` that is used to display the image to the user. This is done by leveraging `ImageQt` provided from `PIL` by casting the edited image into `ImageQt` which can then be passed onto the image label for setting the `QPixMap`
  - The image buffer is reset everytime a new image is opened
- Saving feature is implemented using the built-in `save()` function in the `PIL` library

## How to run

- Install required dependencies using `pip`

```
pip install -r requirements.txt
```

- Or manually install dependencies

  - `pip install PyQt5`
  - `pip install Pillow`

- Run `ImageViewer.py`

```
python ImageViewer.py
```
