import cv2
import numpy as np
import time


def genAvgKernal(kernSize):
    """Fuction to generate an averaging filter

    Args:
        kernSize (interger): filter generated would boe of shape size*size

    Returns:
        numpy_array : generated avg filter
    """

    avgKernal = np.ones((kernSize, kernSize), np.float32) / kernSize**2
    return (avgKernal)


def applyFilter(img, myfilter):
    """Function Convolutes the filter over an image

    Args:
        img (numpy_array): Image on which the filter has to be applied
        myfilter (numpy array): filter kernal

    Returns:
        numpy_array: Convoluted result
    """

    imgH, imgW = np.shape(img)
    filterSize = len(myfilter) 
    pivot = int(filterSize / 2)  # index of pivot location = (int)((size of filter)/2)
    result = np.zeros((imgH - 2 * pivot, imgW - 2 * pivot), np.uint8) # size of convoluted_image= (Height of rawimage-2*pivot)x(Width of of rawimage-2*pivot)
    resultRow = 0
    resultCol = 0
    value = 0

    for imRow in range(pivot, (imgH - pivot)):  # the last row index should be (imgH-1-pivot)
        resultCol = 0
        for imCol in range(
            pivot, (imgW - pivot) ): # the last colomn index should be (imgH-1-pivott)
            value = 0
            for filRow in range(0, filterSize):  # The following two loop traverses through the filter
                for filCol in range(0, filterSize):
                    if filRow > pivot:                     # if filter row index is in the upper half of filter
                        pickR = imRow + (filRow - pivot)   # corresponding  Image row index of raw_image is current image_row + (current filter_row_index - Pivot_row index)
                    else:                                  # if filter row index is in the ceter or  lower half of filter
                        pickR = imRow - (pivot - filRow)   # corresponding  Image row index of raw_image is current image_row - (Pivot_row index - current filter_row_index )
                        
                    if filCol > pivot:                     # if filter column index is in the upper half of filter
                        pickC = imCol + (filCol - pivot)   # corresponding  Image column index of raw_image is current image_column + (current filter_column_index - Pivot_column index)
                        
                    else:                                   # if filter column index is in the upper half of filter
                        pickC = imCol - (pivot - filCol)    # corresponding  Image column index of raw_image is current image_column - ( Pivot_column indexcurrent - filter_column_index)
                        
                    # generating product of filter elements and corresponding image elements
                    value = value + img[pickR][pickC] *  myfilter[filRow][filCol]
            result[resultRow][resultCol] = round(value)
            resultCol += 1
        resultRow += 1
    return result


def zeroPad(img, filterSize):
    """Funtion generates a zeropadded copy of provided image

    Args:
        img (numpy_array): The referance input image to which the zeropadding has to be done
        filterSize (integer): layers of zeros is determined with respect to the size of the filter kernal

    Returns:
        numpy_array: zero padded image
    """
    imgH, imgW = np.shape(img)
    pivot = int(filterSize / 2) # index of pivot location = (int)*((size of filter)/2)
    result = np.zeros((imgH + 2 * pivot, imgW + 2 * pivot), np.uint8) # size of final zero padded image = (raw_image_rows+2*pivot)x(raw_image_columns)
    for r in range(0, imgH):
        for c in range(0, imgW):
            result[r + pivot][c + pivot] = img[r][c]
    return result


def mirrorPad(img, filterSize):
    """function generates a mirror padded copy of provided image

    Args:
        img (numpy_array):
        filterSize (integer): [description]

    Returns:
        numpy_image: mirror padded image
    """

    result = zeroPad(img, filterSize)
    resH, resW = np.shape(result)
    pivot = int(filterSize / 2)

    for row in range(pivot, resH - pivot):
        temp = result[row][pivot + 1:2 * pivot + 1]
        result[row][0:pivot] = temp[::-1]

        temp = result[row][resW - 2 * pivot - 1:resW - pivot - 1]
        result[row][resW - pivot:resW] = temp[::-1]

    for col in range(0, resW):
        temp = result[pivot + 1:2 * pivot + 1, col]
        result[0:pivot, col] = temp[::-1]

        temp = result[resH - 2 * pivot - 1:resH - pivot - 1, col]
        result[resH - pivot:resH, col] = temp[::-1]

    return result


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

################################################# MAIN CODE ############################


IMAGE_PATH = 'data/blur.tif' 

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
