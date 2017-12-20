from debian.debtags import output
from keras.applications.xception import Xception
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.xception import preprocess_input, decode_predictions
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Model
from keras.optimizers import Adamax
import numpy as np

import os
import sys
import glob
import argparse
import matplotlib.pyplot as plt


def get_nb_files(directory):
    """Get number of files by searching directory recursively"""
    if not os.path.exists(directory):
        return 0
    cnt = 0
    for r, dirs, files in os.walk(directory):
        for dr in dirs:
            cnt += len(glob.glob(os.path.join(r, dr + "/*")))
    return cnt

train_dir = "images"
nb_train_samples = get_nb_files(train_dir)
nb_classes = len(glob.glob(train_dir + "/*"))
nb_epoch = 50
batch_size = 20

train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(500,500),
    batch_size=batch_size
)

sgd = Adamax()

model = Xception(weights='imagenet',
                 include_top=False)

input_file = "input.txt"
output_file = "labels.npy"
target = np.load(output_file)

for layer in model.layers[:-1]:
    layer.trainable = False

#model.add(Dense(len(target[0]), activation='softmax'))

x = model.output
x = GlobalAveragePooling2D()(x)
x = Dense(len(target[0]), activation='relu')(x)
predictions = Dense(nb_classes, activation='softmax')(x)
model = Model(input = model.input, output=predictions)

model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

model.fit_generator(
    generator=train_generator,
    samples_per_epoch=nb_train_samples,
    nb_epoch=nb_epoch,
    class_weight='auto'
)
