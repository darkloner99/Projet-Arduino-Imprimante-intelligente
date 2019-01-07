'''
Created on 1 janv. 2019

'''

from Word import Word
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
        while (i<len(self.Word) - 1) :
            im2 = self.Word[i+1].image
            gap = random.randint(150,250)
            height  = getMaxHeight(im1, im2)
            width = getSumWith(im1, im2)
            posH = getHeightPastePos(im1, im2)
            
            new_im = Image.new('L', (width + gap, height))
            new_im.paste(im1,(0,0))
            new_im.paste(im2,(im1.size[0] + gap,posH)) 
            im1 = new_im
            i+=1
            
            
          
        #new_im.show()
            
        self.image = new_im
           
        