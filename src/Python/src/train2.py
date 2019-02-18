
'''
Created on 25 dec. 2018

@author: @antoi
'''


from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, Dropout, Flatten, Dense, Reshape, LSTM
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD,RMSprop,adam
from keras import backend as K
from keras.constraints import maxnorm
from keras.utils import np_utils
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
from PIL import Image
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import cv2
import tensorflow as tf
import keras
#from mnist import MNIST
from keras.models import load_model
from keras.models import model_from_json
from keras import optimizers
from numpy import array



#----------------------------------------------------------------------------------------------#

OUTPUT_PATH = '../data/output/'

characters = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L',
                'M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h',
                'i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','autres']

INPUT_PATH = {
    0:'trie\\0',1:'trie\\1',2:'trie\\2',3:'trie\\3',4:'trie\\4',5:'trie\\5',6:'trie\\6',7:'trie\\7',8:'trie\\8',9:'trie\\9',10:'trie\\A',11:'trie\\B',12:'trie\\C',13:'trie\\D',14:'trie\\E',15:'trie\\F',
    16:'trie\\G',17:'trie\\H',18:'trie\\I',19:'trie\\J',20:'trie\\K',21:'trie\\L',22:'trie\\M',23:'trie\\N',24:'trie\\O',25:'trie\\P',26:'trie\\Q',27:'trie\\R',28:'trie\\S',29:'trie\\T',30:'trie\\U',
    31:'trie\\V',32:'trie\\W',33:'trie\\X',34:'trie\\Y',35:'trie\\Z',36:'trie\\z--a',37:'trie\\z--b',38:'trie\\z--c',39:'trie\\z--d',40:'trie\\z--e',41:'trie\\z--f',42:'trie\\z--g',43:'trie\\z--h',44:'trie\\z--i',45:'trie\\z--j',
    46:'trie\\z--k',47:'trie\\z--l',48:'trie\\z--m',49:'trie\\z--n',50:'trie\\z--o',51:'trie\\z--p',52:'trie\\z--q',53:'trie\\z--r',54:'trie\\z--s',55:'trie\\z--t',56:'trie\\z--u',57:'trie\\z--v',58:'trie\\z--w',59:'trie\\z--x',60:'trie\\z--y',61:'trie\\z--z',
    62:'trie\\autres',
}


#----------------------------------------------------------------------------------------------#


# On charge l'ancien model

# json_file = open('model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)

# loaded_model.load_weights('model.h5')

# model = loaded_model

#----------------------------------------------------------------------------------------------#

model = Sequential()
K.set_learning_phase(1)

model = Sequential()

model.add(Reshape((50,50,1), input_shape=(50*50,)))

model.add(Convolution2D(32, (5,5), input_shape=(50,50,1),activation='relu',padding='same',kernel_constraint=maxnorm(3)))
model.add(Convolution2D(32, (2,2),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.5))

model.add(Convolution2D(32, (5,5),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.5))


model.add(Flatten())


model.add(Dense(1024, activation='relu', kernel_constraint=maxnorm(3)))
model.add(Dense(512, activation='relu', kernel_constraint=maxnorm(3)))
model.add(Dense(256, activation='relu', kernel_constraint=maxnorm(3)))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(63, activation='softmax'))


opt = optimizers.Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0)
model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

print('Model successfully created')
print(model.summary())



def resh(ipar):
    opar = []
    for image in ipar:
        opar.append(image.reshape(-1))
    return np.asarray(opar)


'''
This part of code loaded the new data (Raphael's writing)
we place all image in the same folder and we write the label in the name of the image
we create an array of images and a array of labels ( X_train, Y_train)
'''

total_sample = 0
listing = {}

# Toute les images sont chargé en mémoire et copié dans le même dossier
# On ecrit aussi leur valeurs dans leur nom de fichier
for character, path in INPUT_PATH.items():
    
    # On créer un dictionnaire character => liste des fichiers
    # On compte aussi le nombre de sample
    listing[character] = (os.listdir(path))
    num_sample = len(listing[character])
    total_sample+=num_sample

# Maintenand on va les transférer dans le dossier correspondant 
for character,folder in listing.items():
    
    for files in folder:
        # On  renomme les images et on les colle dans le dossier voulu
        im = cv2.imread(str(INPUT_PATH[character]) + "\\" + str(files))      
        gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
        image = cv2.resize(thresh,(50,50))
        im = np.array(image)
        cv2.imwrite(OUTPUT_PATH + str(character) + " " + str(files),im)
    


# On créer une variable contenat la liste des fichier et une autre mettant en mémoire toutes les images
listing2 = os.listdir(OUTPUT_PATH)
immatrix = array([array(Image.open(OUTPUT_PATH + r"\\" + im2)).flatten() for im2 in listing2],'f')


label = np.ones((len(listing2)),dtype = int)

i = 0
pos_letter = 0
for im in listing2:
        label[i] = int(im[:2])
        i +=1

# On mélange et compile image + nom dans le même tableau
immatrix,label = shuffle(immatrix,label, random_state=2)
train_data = [immatrix,label]

(X, y) = (immatrix,label)
 # on créer les samples de test et d'entrainement
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.0001,random_state=4)

X_train = X_train.reshape(X_train.shape[0], 50*50,1)
X_test = X_test.reshape(X_test.shape[0], 50*50,1)

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

X_train /= 255
X_test /= 255


print('X_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')


X_train = resh(X_train)
X_test  = resh(X_test )

Y_train = np_utils.to_categorical(y_train, 63)
Y_test = np_utils.to_categorical(y_test, 63)



# Now we fit the model 
hist = model.fit(X_train, Y_train, batch_size=30, nb_epoch=45, verbose=1, validation_data=(X_test, Y_test))
hist = model.fit(X_train, Y_train, batch_size=30, nb_epoch=2, verbose=1, validation_split=0.2)



score = model.evaluate(X_test, Y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])


#saves the model info as json file
model_json = model.to_json()
with open("model2.json", "w") as json_file:
    json_file.write(model_json)

# Creates a HDF5 file 'model.h5'    
model.save_weights("model2.h5")

