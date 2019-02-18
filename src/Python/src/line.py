'''
Created on 1 janv. 2019

'''

from word import Word
from Images_utils import getMaxHeight, getSumWith, getHeightPastePos
import random
from PIL import Image


class Line:
    '''
    classdocs
    '''


    def __init__(self,line):
        '''
        Constructor
        '''
        self.Word = []
        self.image = None
        
        self.initWord(line)
        self.linkImage()
        
    def initWord(self,line):
        '''
        Instantiate word 
        '''
        
        for i in range(len(line)):
            word = Word(line[i])
            self.Word.append(word)
    
    def linkImage(self):
        '''
        Create one single image of line with a multitude of words
        '''
        i = 0
        im1 = self.Word[i].image

        # Si il y a plus d'un mot dans la ligne
        if(len(self.Word)> 1):

            while (i<len(self.Word) - 1) :
                im2 = self.Word[i+1].image
                # on prend un espace aléatoire entre 150 et 250 pixels entre les mots
                gap = random.randint(150,250)

                # on calcul les nouvelles dimensions de la ligne 
                height  = getMaxHeight(im1, im2)
                width = getSumWith(im1, im2)
                posH = getHeightPastePos(im1, im2)
                
                # on ajoute a l'image de la ligne le nouveau mot avec l'espace
                new_im = Image.new('L', (width + gap, height))
                new_im.paste(im1,(0,0))
                new_im.paste(im2,(im1.size[0] + gap,posH)) 
                im1 = new_im
                i+=1
            self.image = new_im     

        # Sinon on l'image de la ligne est celle du mot unique
        else:    
            self.image = self.Word[i].image
           
        