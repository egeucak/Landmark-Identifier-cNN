import numpy as np
from numpy import array
import os
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from keras.preprocessing.image import ImageDataGenerator
from time import time
import glob

#location = 'C:/Users/Mavi/PycharmProjects/wc/photographs/Yeni klasör TMM/'
train_dir = '/home/ege/Desktop/machine learning/project/data/Yeni klasör TMM/'

def get_nb_files(directory):
    """Get number of files by searching directory recursively"""
    if not os.path.exists(directory):
        return 0
    cnt = 0
    for r, dirs, files in os.walk(directory):
        for dr in dirs:
            cnt += len(glob.glob(os.path.join(r, dr + "/*")))
    return cnt


train_dir = '/home/ege/Desktop/machine learning/project/data/Yeni klasör TMM/'

nb_train_samples = get_nb_files(train_dir)
nb_classes = len(glob.glob(train_dir + "/*"))
nb_epoch = 200
batch_size = 1

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(40, 40),
    batch_size=batch_size
)

#model = ResNet50(weights="imagenet")
model = Sequential()

model.add(Convolution2D(32, (3, 3), activation='relu', input_shape=(40,40,3)))
model.add(Convolution2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(os.listdir(train_dir)), activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit_generator(
            generator=train_generator,
            steps_per_epoch=nb_train_samples,
            epochs=nb_epoch,
            class_weight='auto',
            shuffle=True
        )



