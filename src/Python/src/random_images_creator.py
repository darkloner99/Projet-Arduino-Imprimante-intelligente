

import os
import random
import numpy as np
import time
import cv2

inpath =  r"C:\Users\antoi\Documents\GitHub\Projet-Arduino-Imprimante-intelligente\src\neuronal-network-handwritting\src\trie\\"

def genereSubRandomImage(im, path):
 """
 Le but est de générer des espaces aléatoires de chaques coté (positifs ou négatifs) afin
 de multiplier le nombre d'images

 """

    id = random.randint(300,54554)

    h, w = im.shape[:2] 

    topBlock_H    = random.randint(0,60) * 5
    rightBlock_W  = random.randint(-7,20) * 5
    bottomBlock_H = random.randint(0,60) * 5
    leftBlock_W   = random.randint(-7,20) * 5


    try:
        htot = h + topBlock_H + bottomBlock_H 
        wtot = w + rightBlock_W + leftBlock_W
        newIm = np.zeros((htot, wtot, 3), np.uint8)
        if(rightBlock_W > 0 and leftBlock_W > 0):
            newIm[topBlock_H:(htot - bottomBlock_H), rightBlock_W:(wtot - leftBlock_W)] = im
            cv2.imwrite(path + str(id) + ".jpg",newIm)

        
        elif(rightBlock_W < 0 and leftBlock_W > 0):
            newIm[topBlock_H:(htot - bottomBlock_H), :(wtot - leftBlock_W)] = im[:h,(-rightBlock_W):w]
            cv2.imwrite(path + str(id) + ".jpg",newIm)


        elif(rightBlock_W > 0 and leftBlock_W < 0):
            newIm[topBlock_H:(htot - bottomBlock_H), rightBlock_W:wtot] = im[:h,:(w - (-leftBlock_W))]
            cv2.imwrite(path + str(id) + ".jpg",newIm)
        
    except:
        pass




def main():
    path = inpath
    subDir = os.listdir(path)

    #List sub Dir like A, B, C ....
    for Dirs in subDir:
        path = inpath + Dirs
        images = os.listdir(path)

        # List images in subDIr
        for image in images:

            path = inpath + Dirs + "\\" + image
            im = cv2.imread(path)

            path = inpath + Dirs + "\\" + image.split(".")[0]

            #Generate 30 clone sub Image 
            for i in range(0,30):
                genereSubRandomImage(im, path)
        print(Dirs + " ----> fini") 
                


main()