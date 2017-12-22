import numpy as np
from numpy import array
import os
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img

#location = 'C:/Users/Mavi/PycharmProjects/wc/photographs/Yeni klasör TMM/'
location = 'C:/Users/Mavi/PycharmProjects/wc/images/images/'

def recursiveDir(location,folders): #gets image paths

    imagePaths = []
    for file in os.listdir(location):
        new_location = location+file
        if ('.jpg' not in file):
            rec_imagePaths, rec_folders = (recursiveDir(new_location+'/',1))
            imagePaths+=rec_imagePaths
            folders+=rec_folders
        else:
            imagePaths.append(new_location)

    return imagePaths, folders

def prepareData(imagePaths): # image to array

    data = []
    for imagePath in imagePaths:
        image = load_img(imagePath, target_size=(28,28),grayscale=True)
        image = img_to_array(image)
        image = image.astype('float32')
        image /= 255
        data.append(image)

    return data

paths, labels_count = recursiveDir(location,0)
data = array(prepareData(paths))

label_names = []
labels = []
for x in paths:
    temp = x.split('/')[-2]
    temp_array = np.zeros((1,labels_count))
    if (temp not in label_names):
        label_names.append(temp)
    index=label_names.index(temp)
    temp_array=temp_array[0]
    temp_array[index]=1
    labels.append(temp_array)
labels = array(labels)

#model = ResNet50(weights="imagenet")
model = Sequential()

model.add(Convolution2D(32, (3, 3), activation='relu', input_shape=(28,28,1)))
model.add(Convolution2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(labels.shape[1], activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

print(data.shape,labels.shape[1])
model.fit(data, labels, batch_size=128, epochs=300, verbose=1)



