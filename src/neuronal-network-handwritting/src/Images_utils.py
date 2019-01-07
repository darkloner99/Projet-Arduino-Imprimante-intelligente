'''
Created on 6 janv. 2019

Ensemble d'outils permettant la manipulation ou l'exploitation de données sur une image
'''

import cv2
import numpy as np
from matplotlib import pyplot as plt
import cv2
import os
from PIL import Image
from time import *
from math import *
#-------------------------------------------------------#
def loadImage(name):
    '''
    Charger une image et applique certains filtres
    '''
    np.set_printoptions(threshold=np.nan)

    image = cv2.imread(name,0)
    image =  cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)

    imgpil = Image.open(name)  
    # Transformation de l'image en tableau numpy5
    img = np.asarray(imgpil) 

    (lenght,larger) = img.shape

    emptyColumns = []
    print(img.shape)

    return image,img,lenght,larger,emptyColumns



def countColumns(array, columns,lenght):
    '''
    Calcule la somme de valeurs des pixel sur une colonne
    '''
    value = 0
    i = 0
    while(i < lenght - 1):
        value = value + array[i][columns]
        i = i + 1

    return value


def calculateAverage(array,X1,X2,lenght):
    '''
    Calcule la somme de pixels entre la colonne X1 et la colonne X2
    '''
    c = X2-X1
    i=0
    value = 0

    while(i < c):
        value = value + countColumns(array,i+X1,lenght)
        i = i+1
        
    return value
        


def calculatePixelDensity(image,img,lenght,larger):
    '''
    Calcule la density de pixel par colonne pour une images (une colonne est égal a une pixel en larger)
    '''
    i = 0
    pixelDensity =[]
    while( i < larger):
        pixelDensity.append(calculateAverage(img,i,i+1,lenght))
        i = i+1
    cv2.imshow("Output", image)
    
    return pixelDensity

def browseDensity(pos,trig,density):
    '''
    Déclancheur si on dépasse un seuil de densité
    '''
    for i in range(pos,len(density) - 1):
        if density[i] >= trig:
            return i
    return i



def cut(density,lenght,image,y,w):
    '''
    Coupe une image
    '''
    roi = image[0:lenght,y:y+w]
    return roi
   

#-------------------------------------------------------#

def countLine(array, columns,larger):
    '''
    Calcule la somme de valeurs des pixel sur une une ligne
    '''
    value = 0
    i = 0
    while(i < larger - 1):
        value = value + array[columns][i]
        i = i + 1

    return value


    

def calculatePixelDensityVertical(img,lenght,larger):
    '''
    Calcule la somme de pixels pour toutes les lignes
    '''
    column = 0
    pixelDensity =[]
    while(column < lenght - 1):
        pixelDensity.append(countLine(img,column,larger))
        column+=1
    
    return pixelDensity


    
def getPeakVecticalPixel(img,lenght,larger):
    '''
    cherche a connaitre la taille et la position d'une lettre ou d'un mot dans une images,
    on souhaite déterminer le "padding" vertical 
    '''
 
    pixelDensity = calculatePixelDensityVertical(img, lenght, larger)
    
    pos1 = 0
    pos2=lenght
    i=0
    try:
        current_value = pixelDensity[0][0]
    except:
        current_value = pixelDensity[0]
        
    while (current_value==0):
        try:
            current_value= pixelDensity[i][0]   
            pos1 = i
            i+=1
        except:
            current_value= pixelDensity[i]
            pos1 = i
            i+=1
            
    i = int(lenght/2)
    
    while i<len(pixelDensity):
        try:
            current_value = pixelDensity[i]
            if current_value==0:
                pos2 = i
            i+=1
        except:
            current_value= pixelDensity[i][0]
            if current_value==0:
                pos2 = i
            i+=1
            
            
    return int((pos2-pos1)/2)
         
        

#-------------------------------------------------------#



def getHeightPastePos(im1,im2):
    '''
    Retourne la position verticale la plus adéquante de la deuxieme image afin de l'aligner 
    au mieux avec la premiere 
    '''
    
    (width1, height1)  = im1.size
    (width2, height2)  = im2.size
    
   

    
        
    np1 = np.asarray(im1)
    np2 = np.asarray(im2)
    pos1 = getPeakVecticalPixel(np1,height1,width1)
    pos2 = getPeakVecticalPixel(np2,height2,width2)
    
    
    return pos1-pos2

    

    
#-------------------------------------------------------#
def getMaxHeight(im1,im2):
    '''
    Retourne la hauteur de l'image la plus haute
    '''
    
    height1= im1.size[1]
    height2 = im2.size[1]
    
    if (height1 > height2):
        maxH = height1
    else:
        maxH = height2

        
        
    return maxH


def getMaxWidth(images):
    '''
    Retourne la largeur de l'image la plus large
    '''
    
    width = 0
    for img in images:
        if img.size[0] > width:
            width = img.size[0]
            
    return width
    
def getSumWith(im1,im2):
    '''
    Retourne la somme des largeurs de 2 images
    '''
    
    width1 = im1.size[0]
    width2 = im2.size[0]
    
    return width1 + width2


def getTotalHeigh(images):
    '''
    Retourne la somme des hauteurs d'un ensemble d'image
    '''
    
    height = 0
    
    for img in images:
        height+= img.size[0]
        
    return height
    
def listToStr(list):
    '''
    Convertie une liste en chaine de character
    '''
    
    string = ""
    for c in list:
        string+=str(c)
        
    return string
        

def add(list,list2):
    '''
    Ajoute deuxieme liste a la premiere
    '''
    for element in list2:
        list.append(element)
        
    return list


    
    
    
    
