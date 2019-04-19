# TODO

* configurable backend endpoint,
* should be able to draw multiple rectagles (labels) per image,
* each rectangle drawn should be shown in a 'label list' in the UI where the user can remove a rectangle if needed,
* the 'label list' only shows rectangles for the current image,
* only submit when changing image, IF any rectangles were added/removed,
* when changing image, redraw all existing rectangles for that image and show them in the 'label list',
* get username/id from AD (e.g. the email address), to be used when submitting labels to the backend,
* a separate tab/pane where all images for a project is listed (thumbnails), separated into 'images with labels' and 'images without labels',
* clicking on an image in the overview tab/pane should start labeling from that image, and going 'left' shows the previous image, and 'right' the next, just like the main tab/pane is doing.
* support keyboard commands such as 'c' for clearing all labels for the current image, 'z' for undoing the rectangle that was just drawn, and 0-9 for choosing the 'class' associated with the latest rectangle that was drawn (default to class 0),
* allow the mouse to leave the canvas and continue to draw (the rectangle still being inside the image but still tracking the mouse)

