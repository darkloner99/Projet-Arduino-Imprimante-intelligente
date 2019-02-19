
'''
Created on 30 dec. 2018


Une page d'ecriture est généré a partir de ce code, Page se contente de triéer les combinaisons et de les indexer 
et et d'appeler la classe ligne afin de récuperer des images de lignes et par la suite de les coller

'''

#List containing all known combinations
sequence_letters = []
#List containing images of all know combinations
sequence_files = []

#----------------------------------------------------------------------------------------------#  
import os
import numpy as np
import re
import time

from line import Line
from Images_utils import getTotalHeigh, getMaxWidth
from PIL import Image
from data import *
import data
    
#----------------------------------------------------------------------------------------------#   

class Page:
    '''
    classdocs
    '''

    
    def __init__(self, text):
        '''
        Constructor
        '''
        self.text = text
        self.Lines = []
        self.Lines_images = []
        self.image = None
        Page.sort_link()
        Page.generate(self)
        
        
        
    
    def generate(self):
        '''
        Instantiate line 
        '''

        # On separe le text en ligne
        lines = self.splitText()
        # On instancie ses lignes et on les stocke
        for i in range(len(lines)):
            line = Line(lines[:][i])
            self.Lines.append(line)
            self.Lines_images.append(line.image)
            
        # On calcule la taille des lignes
        totalHeight = getTotalHeigh(self.Lines_images) + 2*150
        width = getMaxWidth(self.Lines_images) + 2*200
        gap = 20
        totalHeight+=gap*len(self.Lines)  
        #new_im = Image.new('RGB',(totalHeight,width))
        new_im = Image.new('RGB',(2480*4,3508*4))
        
        # On créer la page en collant chaque image de ligne
        pos = 150
        for i in range(len(self.Lines)):
            img = self.Lines[i].image
            #img.show()
            current_height = img.size[1]
            new_im.paste(img,(150,pos + gap + current_height))
            pos+=current_height + 270
            
        #new_im.show()
        #time.sleep(30)
        self.image = new_im
                
            
        
        
            
        
        
    def splitText(self):
        '''
        Slit text in a multitude of line 
        '''
        # Remplace les ".", "," par des retours a la ligne
        # Tout les caractères recurrents et non souhaités sont remplacer
        self.text = self.text.replace('\'',' ')
        self.text =  self.text.replace('.',' \n ')
        self.text =  self.text.replace('!',' \n ')
        self.text =  self.text.replace('?',' \n ')
        self.text =  self.text.replace(',',' \n ')
        self.text =  self.text.replace('\n',' \n ')

        text_splitted = self.text.split(" ")
        
        counter = 0
        line = []
        buffer_line = []
        # on veut des lignes avec max : 35  charactères
        for words in text_splitted:
            # Si on a un saut a la ligne
            if(words == "\n"):
                if(buffer_line!=[]):
                    line.append(list(buffer_line))
                    buffer_line = []
                    counter = 0

            # Si on ne depasse pas les 35 charactères sur une ligne
            elif(counter + len(words) <= max_line_lenght):
                if(words !="" and words !=" "):
                    buffer_line.append(words)
                    counter = counter + len(words)
                
            # Sinon on ajoute la ligne temporaire a l'ensemble des lignes
            else:
                line.append(list(buffer_line))
                buffer_line = []
                if(words !="" and words !=" "):
                    buffer_line.append(words)
                    counter = 0

        # Cette ligne est nécessaire afin d'ajouter la derniere ligne 
        # temporaire à l'ensemble des lignes 
        if(buffer_line!=[]):     
            line.append(buffer_line)
            
        return line
        
                        
    
    
    #--------------------------------------------------------------------------------#   
    @staticmethod
    def sort_link():
        '''
        Initialize sequence_letters and sequence_files
        
        sequence_letters regroupe des combinaisons de lettres (deux, trois, quatres, etc...) que,
        l'on peut attacher pour faire une écriture cursive
        
        sequence_files regroupe les fichiers images liés a sequence_letters
        '''
        
        lfiles = []
        lfolders = []
        lsequence = []
        global sequence_files
        global sequence_letters
        
        # On liste l'ensemble des fichiers images
        for folder,subfolder,files in os.walk(characters2):
            if (len(files)<1):
                pass
                
            else:
                lfiles.append(files)
                lfolders.append(folder)
               
        # data est un tableau a deux dimensions, pour chaques fichiers on a son dossier parent  
        data = zip(lfiles,lfolders)
        
        
        sequence = ""
        buffer =""
        prev_pos = 0
        curr_pos = 0
        lenght = 0
        link = 0
        lsequence_files = []
       
        # on traite toutes les images
        for files,folder in data:
            
            i = 0
            prev_pos = 0
            lenght = len(files)
            lbuffer_files = []
            
            
            for file in files:
                
                # chaques fichier a dans son nom des caractéristique qu'on recupère afin de trier  
                footprint =  re.findall(r"[0-9]*-([0-9]*)-([a-z]*)(-*).*",file)
                try:
                    buffer =  footprint[0][1]
                    lbuffer_files.append(folder +"\\" + file)
                    curr_pos  = int(footprint[0][0])
                    
                    # un tirer signifie que l'image doit etre attacher a la suivante 
                    if (footprint[0][2] == '-'):
                        sequence= sequence + buffer
                        link+=1
                        
                    # si on est au premier charactère
                    elif(i==0):
                        sequence= sequence + buffer
                        
                    # si l'espace entre les 2 charactère est petit
                    elif(curr_pos-prev_pos < 150):
                        sequence= sequence + buffer
                        
                    # Si on a au moins un charactère précedent lié et que maintenant ce n'est plus le cas
                    if ((link>=1 and footprint[0][2] != '-')):
                        # on ajoute alors la sequence temporaire 
                        if len(sequence) >1:
                            lsequence.append(sequence)
                            lsequence_files.append(lbuffer_files)
                            lbuffer_files = []
                       
                            sequence= ""
                            
                        else:
                            sequence= ""
                        
                        link = 0
                    # Si on arrive au bout de la chaine ou on a un lien a faire avec la lettre suivante
                    elif (i == (lenght -1 ) or (footprint[0][2] != '-' and (curr_pos-prev_pos) >= 150)):
                        
                        #Si a plus d'un charactere dans la sequence
                        if len(sequence) >1:
                            #on recupere tout les combinaisons de lettre faisable avec les fichiers correspondant 
                            combinations_letters,combination_files = Page.split_combination(sequence,lbuffer_files,folder)
                            for combination,files in zip(combinations_letters,combination_files):
                                lsequence.append(combination)
                                lsequence_files.append(files)
                            sequence= ""
                            lbuffer_files = []
                            
                        else:
                            sequence= ""
                            lbuffer_files = []
                        
                        
                        
                except:
                    print("Error")
                    pass
                
                i+=1
                prev_pos = curr_pos
        sequence_letters = list(lsequence)
        sequence_files = list(lsequence_files)

        
    @staticmethod   
    def split_combination(sequence,lbuffer_files,folder):
        '''
        Extension of sort-link in order to initialize sequence_letters and sequence_files
        
        Créer une multitude de combinaisons a partir d'une seule combinaisons de lettres si elle ne sont pas
        liées (pas de '-' dans le nom du fichier )
        '''
        
        i = 0
        combinations_letters = []
        combination_files = []
        chain =""
        files = []
        
        while (i<len(sequence)):
            chain = sequence[i]
            files = []
            files.append(lbuffer_files[i])
            
            for next,file in zip(sequence[(i+1):],lbuffer_files[(i+1):]):
                
                chain+=next
                files.append(file)
                
                combinations_letters.append(chain)
                combination_files.append(list(files))
                
            i+=1
        return combinations_letters,combination_files
                    
    #--------------------------------------------------------------------------------#              
                
                  


