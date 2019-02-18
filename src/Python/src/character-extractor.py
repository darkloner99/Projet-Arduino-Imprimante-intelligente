'''
Created on 22 dec. 2018

@author: @antoi
'''
from keras.models import load_model
from keras.models import model_from_json
import cv2
import numpy as np
from matplotlib import pyplot as plt
import cv2
import os


# On charge le model qui permet d'évaluer les lettres et de les classifier
json_file = open('model2.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights('model2.h5')
model = loaded_model

print('Model successfully loaded')



from Images_utils import loadImage, countColumns, calculateAverage, calculatePixelDensity, browseDensity, cut

#-------------------------------------------------------#

characters = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','autres']

PATH=r'C:\Users\antoi\Documents\GitHub\Projet-Arduino-Imprimante-intelligente\src\neuronal-network-handwritting\src\page-5-extraction\\'

#-------------------------------------------------------#

def evalue(image):
	#This method predict the input image and return it
	
    height, width, depth = image.shape

    #resizing the image to find spaces better
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    image = cv2.resize(thresh,(50,50))
    cv2.imshow("Image",image)
    roi = np.array(image)
    t = np.copy(roi)
    t = t / 255.0
    t = t.reshape(1,2500)
	#predit image
    pred = model.predict_classes(t)
    return(characters[int(pred)])
   

#-------------------------------------------------------#



'''
The algorithm takes a part of the image, if it does not detect a 
character it reduces the margin, finally if it detects a character, 
it goes to the border of the cuted image and it analyzes the next one. 
We could call that a sweeping method
'''
    	
def main():
	pos = 0 
	compt_file = 0
	
	# Images are firstly in the same folder
	files = os.listdir(PATH)
	
	
	for file in files:
		pos = 0 
		compt_file+=1
		print("----------")
		print("file " + str(compt_file) + " on " + str(len(files)))
		dirname = PATH + str(file)[:5] + "split\\"

		#we create a subfolder where after we will place the predicted characters in different image that we can 
		#collapse it
		os.mkdir(dirname)

		#load image and copy into the subfloder
		image,img,lenght,larger = loadImage(PATH+str(file))
		cv2.imwrite(dirname + str(file), image )

        
		density = calculatePixelDensity(image,img,lenght,larger)
		pos = browseDensity(pos,100,density)
		compt_letters = 0
		w = 130
		#On parcourt l'image par balayge en essayant de détecter des charactères 
		while(pos < larger):
			roi = cut(density,lenght,image,pos,w)
			#Evalue image
			value = evalue(roi)
			if (value!='autres'):
				#En rentrant dans ce if on confirme qu'on a détecté une lettre
				#On sauve l'image et on reinitialise les paramètres de balayage
				filename = dirname + str(compt_letters) +"-"+ str(int((pos+(pos+w))/2)) + "-" + value +".jpg"
				compt_letters+=1
				cv2.imwrite(filename,roi)
				pos = pos + w 
				w = 130

			if w == 50:
				pos = pos + 1
				w = 130

			else:
				w = w-1

        
main()





    

