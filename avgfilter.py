import cv2
import numpy as np 

def genAvgKernal(kernSize): #genAvgKernal(kernSize) returns  a averaging filter kernal of size 'kernSize'
    avgKernal = np.ones((kernSize,kernSize),np.float32)/kernSize**2
    return avgKernal
   
def applyFilter(img,myfilter):
    imgH,imgW = np.shape(img)
    filterSize = len(myfilter)
    pivot = int(filterSize/2)
    result = np.zeros((imgH-2*pivot,imgW-2*pivot),np.uint8)
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
    
            
     
img_grey = cv2.imread('data/blur.tif',cv2.IMREAD_GRAYSCALE) 
result_img_1=applyFilter(img_grey,genAvgKernal(3))
cv2.imshow('Output',img_grey)
cv2.imshow('filtered',result_img_1)
cv2.waitKey(0)