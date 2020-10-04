import cv2
import numpy as np 
import time
def genAvgKernal(kernSize): #genAvgKernal(kernSize) returns  a averaging filter kernal of size 'kernSize'
    avgKernal = np.ones((kernSize,kernSize),np.float32)/kernSize**2
    return avgKernal
   
def applyFilter(img,myfilter):#convolutes  myfilter and img and resturns the convoluted resultant matrics 
    imgH,imgW = np.shape(img) #save the height and width of the image 
    filterSize = len(myfilter) #get the filter size
    pivot = int(filterSize/2) #pivot or core of filter 
    result = np.zeros((imgH-2*pivot,imgW-2*pivot),np.uint8) # a result matrix to store the convolution result
    resultRow = 0
    resultCol = 0
    value = 0
    for imRow in range(pivot,(imgH-pivot)): #the last row index should be (imgH-1-pivot)
        resultCol = 0
        for imCol in range(pivot,(imgW-pivot)):#the last colomn index should be (imgH-1-pivott)
            value = 0
            for filRow in range(0,filterSize):
                for filCol in range(0,filterSize):
                    if filRow > pivot :
                        picLocRow = imRow + (filRow -pivot )
                    else:
                        picLocRow = imRow - (pivot - filRow)
                    if filCol > pivot:
                        picLocCol = imCol + (filCol - pivot)
                    else:
                        picLocCol = imCol - (pivot - filCol)
                    value = value + img[picLocRow][picLocCol]*myfilter[filRow][filCol]       
            result[resultRow][resultCol] = round(value)
            resultCol+=1
        resultRow+=1
    return result


def zeroPad(img,filterSize):
    imgH,imgW = np.shape(img) #save the height and width of the image  #get the filter size
    pivot = int(filterSize/2) #pivot or core of filter 
    result  = np.zeros((imgH+2*pivot,imgW+2*pivot),np.uint8)
    for r in range(0,imgH):
        for c in range(0,imgW):
            result[r+pivot][c+pivot]=img[r][c]
    return result
        
def mirrorPad(img,filterSize):
    result = zeroPad(img,filterSize)
    resH,resW = np.shape(result)
    pivot = int(filterSize/2)
    for row in range(pivot,resH-pivot):
        temp =  result[row][pivot+1:2*pivot+1]
        result[row][0:pivot] = temp[::-1]
        
        temp =result[row][resW-2*pivot-1:resW-pivot-1]
        result[row][resW-pivot:resW] = temp[::-1]
    
    for col in range(0,resW):
        temp = result[pivot+1:2*pivot+1,col]
        result[0:pivot,col] = temp[::-1]  

        temp = result[resH-2*pivot-1:resH-pivot-1,col]
        result[resH-pivot:resH,col] = temp[::-1]

    return result


def getSize():
    return int(input("Enter filter size (example - input '3' to gen 3*3 filter): "))

def mainMenu():
    menu = {1:'Mirroring' , 2:'Zero padding' , 3:'Crop-off' ,4:'Change filter size',5:'Exit'}
    print("\n\n{:^40}\n{:^40}\n".format('MENU','======'))
    for key,option in menu.items():
        print('{:>17} {}\n'.format('('+str(key)+')',option))
    choice = int(input("Awaiting response.. : "))
    if choice not in menu.keys():
        print("invalid response!!")
        time.sleep(2)
        mainMenu()
    return choice
  
img_grey = cv2.imread('data/gear.jpg',cv2.IMREAD_GRAYSCALE) 
size = getSize()
while True:
    avgFilter = genAvgKernal(size)
    response = mainMenu()
    if response == 1 :
        print("Mirror padding the image...")
        mirrored_img = mirrorPad(img_grey,size)
        print("Mirror Padding complete!!\nApplying filter...")
        filtered_img = applyFilter(mirrored_img,avgFilter)
        print("Filter Applied!!")
    elif response == 2 :
        print("Zero padding the image...")
        zeropadded_img = zeroPad(img_grey,size)
        print("Zero Padding complete!!\nApplying filter...")
        filtered_img = applyFilter(zeropadded_img,avgFilter)
        print("Filter Applied!!")
    elif response == 3 :
        print("Applying filter...")
        filtered_img = applyFilter(img_grey,avgFilter)
        print("Filter Applied image cropped!!")
    elif response == 4 :
        size = getSize()
        continue
    elif response == 5 :
        print("Application closed")
        exit()
    
    cv2.namedWindow('Raw Image',cv2.WINDOW_NORMAL)
    cv2.namedWindow('Filtered Image',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Raw Image',800,800)
    cv2.resizeWindow('Filtered Image',800,800)
    

    cv2.imshow("Raw Image",img_grey)
    cv2.imshow("Filtered Image",filtered_img)
    print("Press ESC to go back to menus")
    key = cv2.waitKey(0)
    if key ==  27:
        cv2.destroyAllWindows()
print("Application Closed")


