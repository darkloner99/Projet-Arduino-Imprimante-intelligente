
'''
Created on 24 dec. 2018

@author: shubhammor0403
and adapted by @antoi
'''


from keras.models import Sequential
from keras import optimizers
from keras.layers import Convolution2D, MaxPooling2D, Dropout, Flatten, Dense, Reshape, LSTM
from keras import backend as K
from keras.constraints import maxnorm
from keras.utils import np_utils
import tensorflow as tf
import keras
import matplotlib
import numpy as np
from mnist import MNIST
import cv2
from keras.models import load_model
from keras.models import model_from_json
from matplotlib import pyplot as plt


print("loading data...")


mndata = MNIST(r'C:\Users\antoi\Documents\GitHub\Projet-Arduino-Imprimante-intelligente\src\datasets\gzip')
mndata.select_emnist('byclass')
#This will load the train and test data
X_train, y_train = mndata.load_training()
                
X_test, y_test = mndata.load_testing()

# Convert data to numpy arrays and normalize images to the interval [0, 1]
X_train = np.array(X_train)  / 255.0
y_train = np.array(y_train)
X_test = np.array(X_test) / 255.0
y_test = np.array(y_test)

#Reshaping all images into 28*28 for pre-processing
X_train = X_train.reshape(X_train.shape[0], 28, 28)
X_test = X_test.reshape(X_test.shape[0], 28, 28)

#Reshaping all images to enter in neuronal network
X_train = X_train.reshape(X_train.shape[0], 784,1)
X_test = X_test.reshape(X_test.shape[0], 784,1)



def resh(ipar):
    opar = []
    for image in ipar:
        opar.append(image.reshape(-1))
    return np.asarray(opar)



train_images = X_train.astype('float32')
test_images = X_test.astype('float32')

train_images = resh(train_images)
test_images = resh(test_images)


train_labels = np_utils.to_categorical(y_train, 63)
test_labels = np_utils.to_categorical(y_test, 63)

#Create the network 
K.set_learning_phase(1)

model = Sequential()

model.add(Reshape((28,28,1), input_shape=(784,)))

model.add(Convolution2D(32, (5,5), input_shape=(28,28,1),activation='relu',padding='same',kernel_constraint=maxnorm(3)))
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


#fit the model on train data
print(model.summary())
history = model.fit(train_images,train_labels,validation_data=(test_images, test_labels), batch_size=62, epochs=20)

#evaluating model on test data
scores = model.evaluate(test_images,test_labels, verbose = 0)    
print("Accuracy: %.2f%%"%(scores[1]*100))



print(history.history.keys())

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.grid()
plt.show()


# Saves the model info as json file
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
    
# Creates a HDF5 file 'model.h5'
model.save_weights("model.h5")
