import os
import cv2
import numpy as np 
import time

'''
Created on 21 dec. 2018
this code has been inspired by @gladiator (stackOverflow user) to extract characters and words in images

@author:  @antoi
'''

#-------------------------------------------------------------------------------#

inpath = r"C:\Users\antoi\Documents\Code\python\imprimante\new\texte\data4\\"
outpath =r"C:\Users\antoi\Documents\Code\python\imprimante\new\texte\data4\\"
count = 0

#-------------------------------------------------------------------------------#

def transform(image, kernel):
    
    
    morph = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    
    gray = cv2.cvtColor(morph,cv2.COLOR_BGR2GRAY)
    
    #salt = cv2.fastNlMeansDenoising(gray,None,9,16)

    ret,thresh= cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
    
    return thresh




def getWritting(image):

    global count
    image = cv2.imread(image)
    print(r"Input info:")

    
    
    print(image.shape)
        
    
    #---------------------------#
    # Localize line in page     #
    #---------------------------#
    
    # Look image better in order to work on 
    kernel = np.ones((2,2),np.uint8)
    thresh = transform(image,kernel)
    
    # Dilate and detect contours
    kernel = np.ones((5,500), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    im2,ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
    
    print(r"generating...")
    
    for i, ctr in enumerate(sorted_ctrs):

        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)
    
        # Getting ROI
        roi = image[y:y+h, x:x+w]
    
        im = cv2.resize(roi,None,fx=4, fy=4, interpolation = cv2.INTER_CUBIC)
        
         #---------------------------#
         # Localize words in line    #
         #---------------------------#
         
        # Look image better in order to work on 
        kernel = np.ones((10,10),np.uint8)
        thresh_im = transform(im, kernel)
        
        # Dilate and detect contours
        kernel = np.ones((20, 40), np.uint8)
        words = cv2.dilate(thresh_im, kernel, iterations=1)
        im,ctrs_1, hier = cv2.findContours(words, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        sorted_ctrs_1 = sorted(ctrs_1, key=lambda ctr: cv2.boundingRect(ctr)[0])
        
        for j,ctr_1 in enumerate(sorted_ctrs_1):

            # Get bounding box
            x_1, y_1, w_1, h_1 = cv2.boundingRect(ctr_1)
            
            cv2.rectangle(thresh_im,(x_1,y_1),(x_1+w_1,y_1+h_1),(0,0,255),3)

    
            # Getting ROI
            roi_1 = thresh_im[y_1:y_1+h_1, x_1:x_1+w_1]
    
            #---------------------------#
            # Apply filter and save img #
            #---------------------------#
            # # Image like comma are not important, so their are not saved
            
            size = len(roi_1)
            if size > 200:   # apply filter: 100 character, 300 words
                path = outpath + str(count) + ".jpg"
                cv2.imwrite(path, roi_1)
                count = count + 1

        
    print(r"end generating...")
    print(r"Counter:")
    print(count)



def main():
    imageCounter = 0
    filesInDir = os.listdir(inpath)
    for image in filesInDir:
        imageCounter = imageCounter + 1
        print("------------------------")
        print(str(imageCounter) + r" images sur " + str(len(filesInDir)))
        print("Nom:" + image)
        path = inpath + image
        getWritting(path)
        
        
main()