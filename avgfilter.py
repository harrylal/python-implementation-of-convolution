import cv2
import numpy as np 

def genAvgKernal(kernSize): #genAvgKernal(kernSize) returns  a averaging filter kernal of size 'kernSize'
    avgKernal = np.ones((kernSize,kernSize),np.float32)/kernSize**2
    return avgKernal
   
def applyFilter(img,myfilter):
    imgH,imgW = np.shape(img)
    filterSize = len(myfilter)
    pivot = int(filterSize/2)
    result = np.zeros((imgH-pivot,imgW-pivot),np.float32)
    resultRow = 0
    resultCol = 0
    value = 0
    for imRow in range(pivot,(imgH-pivot)): #the last row index should be (imgH-1-pivot)
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
                    result[resultRow][resultCol] = value 
        resultCol+=1
    resultRow+=1
    return result
    
            
     
img_grey = cv2.imread('data/blur.tif',cv2.IMREAD_GRAYSCALE)
# result_img=applyFilter(img_grey,genAvgKernal(3))
result_img = cv2.filter2D(img_grey,-1,genAvgKernal(3))
print(img_grey) 
print(result_img)
print(np.shape(result_img))
# print(np.shape(img_grey))
cv2.imshow('Ouput',result_img)
cv2.waitKey(0)