'''
Created on 1 janv. 2019

'''
from data import *
import os
import random
from PIL import Image
from Images_utils import getMaxHeight, getSumWith, getHeightPastePos
import data
from Images_utils import listToStr, add
import copy


class Word:
    '''
    classdocs
    '''
    buffer_files = []

    def __init__(self, word):
        '''
        Constructor
        '''
        
        self.Character = []
        self.names = []
        self.image = None
        
        self.initLetter(word)
        self.constructWord()
        self.linkImage()
        print("\n")
        
    
    def initLetter(self,word):
        '''
        self.Character = word
        '''
        
        for i in range(len(word)):
            self.Character.append(word[i])
            
        
    def searchPattern(self,pattern):
        '''
        Return true if the pattern is in sequence_letters
        '''
        from Page import sequence_letters
        
        for combinaison in sequence_letters:
            if (pattern == combinaison):
                return True
    
        return False
    
    def getPattern(self,pattern):
        '''
        Return the corresponding pattern in image
        '''
        from Page import sequence_files,sequence_letters
        
        files = None
        for combinaison in sequence_letters:
                if pattern == combinaison:
                    n = sequence_letters.index(combinaison)
                    files = list(sequence_files[n])
                    print(str(combinaison) + " : " + str(files))
                    break
    
        return files
    
    
    
    def getRandomCharacterImage(self,c):
        '''
        Return a random images corresponding to the character
        '''
        
        i = characters.index(c)
        subfolder = INPUT_PATH[i]
        files = os.listdir("../data/charac/" + subfolder)
        number  = random.randint(0,len(files)-1)
        
        print(str(c) + " : " + str(files[number]))
        return "../data/charac/" + subfolder + "/" + files[number]
        
    
    
    
    def constructWord(self):
        '''
        Construct the word, create a list of separate images
        '''
        i = 0
        n = 0
        prev_pattern=None
        while i <len(self.Character) and n<len(self.Character):
            
            while True:
                pattern = listToStr(self.Character[i:n+2])
                
                if(not self.searchPattern(pattern) and prev_pattern!=None):
                    self.names = add(self.names,self.getPattern(prev_pattern))
                    prev_pattern = None
                    i = n
                    n = n + 1
                    break  
                elif self.searchPattern(pattern):        
                    prev_pattern = pattern          
                    n = n + 1            
                else:
                    self.names.append(self.getRandomCharacterImage(self.Character[i]))
                    n = n + 1
                    break
                if (n+1 >= len(self.Character)):
                    self.names = add(self.names,self.getPattern(pattern))
                    prev_pattern = None
                    if (n-i)<=2:
                        n = n + 1
                    else:
                        n=i+2
                    break
                         
            i+=1
    

    
    
    def linkImage(self):
        '''
        Collapse all images to create one single image's word
        '''
        
        images = []
        for name in self.names:
            images.append(Image.open(name))
            
        i = 0
        im1 = images[i]
        while i<len(images) - 1 :
            im2 = images[i+1]
            gap = random.randint(10,30)
            width = getSumWith(im1, im2)
            height  = getMaxHeight(im1, im2) 
            #posH = getHeightPastePos(im1, im2)
            
            new_im = Image.new('RGB', (width,height)).convert('LA')
            new_im.paste(im1,(0,int((height-im1.size[1])/2)))
            new_im.paste(im2,(im1.size[0]-10,int((height-im2.size[1])/2))) 
            im1 = new_im
            #im1.show()
            i+=1
            
        self.image = im1
           
            
    
    
    