'''
@author: @antoi

This code add black space around and image.I uses it ajust the height of the letters
'''
import os
import random
import numpy as np
import time
import cv2

inpath =  r"C:\Users\antoi\Documents\GitHub\Projet-Arduino-Imprimante-intelligente\src\neuronal-network-handwritting\data\charac\trie\z--l\\"

def addBlack(im, path, topBlock_H, bottomBlock_H, rightBlock_W, leftBlock_W):



    h, w = im.shape[:2] 

    # Suivant les valeurs positives ou négative de rightBlock_W et leftBlock_W 
    # on procede d'une maniere ou d'un autre afin d'ajouter ou d'enlever une partie

    # Attention: ce code est en grosse partie copié du code @random_images_creator.py avec 
    # quelques modifications. Il a été testé uniquement afin d'ajouter une zone noir en haut ou
    # en bas de l'image
    #
    try:
        htot = h + topBlock_H + bottomBlock_H 
        wtot = w + rightBlock_W + leftBlock_W
        newIm = np.zeros((htot, wtot, 3), np.uint8)
        if(rightBlock_W >= 0 and leftBlock_W >= 0):
            newIm[topBlock_H:(htot - bottomBlock_H), rightBlock_W:(wtot - leftBlock_W)] = im
            cv2.imwrite(path +".jpg",newIm)

        
        elif(rightBlock_W < 0 and leftBlock_W > 0):
            newIm[topBlock_H:(htot - bottomBlock_H), :(wtot - leftBlock_W)] = im[:h,(-rightBlock_W):w]
            cv2.imwrite(path +".jpg",newIm)


        elif(rightBlock_W > 0 and leftBlock_W < 0):
            newIm[topBlock_H:(htot - bottomBlock_H), rightBlock_W:wtot] = im[:h,:(w - (-leftBlock_W))]
            cv2.imwrite(path + ".jpg",newIm)
        
    except:
        pass



def main():
    Dir = os.listdir(inpath)

    # List images in DIr
    for image in Dir:

        path = inpath + "\\" + image
        im = cv2.imread(path)

        path = inpath +"\\" + image.split(".")[0]    
        addBlack(im,path,0,40,0,0)
        print(image + " ----> fini") 
            


main()