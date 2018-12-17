import tensorflow as tf

import numpy as np
from mnist import MNIST
from matplotlib import pyplot as plt


#This initialize MNIST class
mndata = MNIST(r'C:\Users\antoi\Documents\GitHub\Projet-Arduino-Imprimante-intelligente\src\datasets\gzip')
mndata.select_emnist('byclass')


#This will load the train and test data
X_train, y_train = mndata.load_training()
                
X_test, y_test = mndata.load_testing()

# Convert data to numpy arrays and normalize images to the interval [0, 1]
X_train = np.array(X_train) 
y_train = np.array(y_train)
X_test = np.array(X_test) 
y_test = np.array(y_test)

#Reshaping all images into 28*28 for pre-processing
X_train = X_train.reshape(X_train.shape[0], 28, 28)
X_test = X_test.reshape(X_test.shape[0], 28, 28)


print('Tabloids length: '")
print(X_train.shape) 
print(y_train.shape)



ROW = 4
COLUMN = 5
for i in range(ROW * COLUMN):
    # train[i][0] is i-th image data with size 28x28
    image = X_train[i]  
    image = np.array(image,dtype='uint8')
    plt.subplot(ROW, COLUMN, i+1)          # subplot with size (width 4, height 5)
    plt.imshow(image, cmap='gray')  # cmap='gray' is for black and white picture.
    plt.axis('off')  # do not show axis value
    plt.title('label = {}'.format(y_train[i]))
plt.tight_layout()   # automatic padding between subplots
plt.show()