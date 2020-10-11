import cv2
import time
from avgfilter import *

IMAGE_PATH = 'data/gear.jpg'


def getSize():  # Asks the user for an input and returns the input
    return int(
        input("Enter filter size (example - input '3' to gen 3*3 filter): "))


def mainMenu():  # Displays a menu on the output window and returns the choice  selected by the user
    menu = {
        1: 'Mirroring',
        2: 'Zero padding',
        3: 'Crop-off',
        4: 'Change filter size',
        5: 'Exit'}
    print("\n\n{:^40}\n{:^40}\n".format('MENU', '======'))
    for key, option in menu.items():
        print('{:>17} {}\n'.format('(' + str(key) + ')', option))
    choice = int(input("Awaiting response.. : "))
    if choice not in menu.keys():
        print("invalid response!!")
        time.sleep(2)
        mainMenu()
    return choice
 

img_grey = cv2.imread(IMAGE_PATH, cv2.IMREAD_GRAYSCALE)
size = getSize()

while True:
    avgFilter = genAvgKernal(size)
    response = mainMenu()
    if response == 1:
        print("Mirror padding the image...")
        mirrored_img = mirrorPad(img_grey, size)
        print("Mirror Padding complete!!\nApplying filter...")
        filtered_img = applyFilter(mirrored_img, avgFilter)
        print("Filter Applied!!")
    elif response == 2:
        print("Zero padding the image...")
        zeropadded_img = zeroPad(img_grey, size)
        print("Zero Padding complete!!\nApplying filter...")
        filtered_img = applyFilter(zeropadded_img, avgFilter)
        print("Filter Applied!!")
    elif response == 3:
        print("Applying filter...")
        filtered_img = applyFilter(img_grey, avgFilter)
        print("Filter Applied image cropped!!")
    elif response == 4:
        size = getSize()
        continue
    elif response == 5:
        print("Application closed")
        exit()

    # Window to display raw image and filtered image
    cv2.namedWindow('Raw Image', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Filtered Image', cv2.WINDOW_NORMAL)
    
    # Resize both windows, to avoid case when the images are too big to be displayed
    cv2.resizeWindow('Raw Image', 800, 800)
    cv2.resizeWindow('Filtered Image', 800, 800)

    # Display the image in the respective windows
    cv2.imshow("Filtered Image", filtered_img) 
    cv2.imshow("Raw Image", img_grey)

    print("Press ESC to go back to menus")
    key = cv2.waitKey(0)
    if key == 27:                                          # 27 corresponds to ESC
        cv2.destroyAllWindows()
print("Application Closed")