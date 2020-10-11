import cv2
from avgfilter import *

IMAGE_PATH = 'data/gear.jpg'

def getSize():  # Asks the user for an input and returns the input
    return int(input("Enter filter size (example - input '3' to gen 3*3 filter): "))

img_grey = cv2.imread(IMAGE_PATH, cv2.IMREAD_GRAYSCALE)
size = getSize()

# Window to display raw image and filtered image
cv2.namedWindow('Raw Image', cv2.WINDOW_NORMAL)
cv2.namedWindow('Zero Padded', cv2.WINDOW_NORMAL)
cv2.namedWindow('Mirror Padded', cv2.WINDOW_NORMAL)
    
# Resize both windows, to avoid case when the images are too big to be displayed
cv2.resizeWindow('Raw Image', 800, 800)
cv2.resizeWindow('Zero Padded', 800, 800)
cv2.resizeWindow('Mirror Padded',800, 800)

# Display the image in the respective windows
cv2.imshow('Raw Image', img_grey)
cv2.imshow('Zero Padded', zeroPad(img_grey, size))
cv2.imshow('Mirror Padded', mirrorPad(img_grey, size))

print("Press ESC to go back to exit")
key = cv2.waitKey(0)
if key == 27:                                          # 27 corresponds to ESC
    cv2.destroyAllWindows()
print("Application Closed")