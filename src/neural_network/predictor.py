from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.preprocessing.image import ImageDataGenerator
import keras
from keras.optimizers import SGD
import os
import glob

import numpy as np
import cv2
from skimage.transform import resize

places_names = np.load("place_names.npy")

def encode_prediction(pred, n):
    pred = pred[0]
    ind = np.argpartition(pred, -n)[-n:]
    ind = ind[np.argsort(pred[ind])[::-1]]
    show = lambda perc, index : "{} -> {:2f}%".format(places_names[index], perc*100)
    return list(map(show, pred[ind], ind))

base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224,224,3))

# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
x = Dense(1024, activation='relu')(x)
# and a logistic layer -- let's say we have 176 classes
predictions = Dense(176, activation='softmax')(x)

# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

for layer in base_model.layers:
    layer.trainable = False

model.load_weights("weights.hdf5")


for layer in model.layers[:153]:
   layer.trainable = False
for layer in model.layers[153:]:
   layer.trainable = True

# we need to recompile the model for these modifications to take effect
# we use SGD with a low learning rate

sgd = SGD(lr=0.0001, momentum=0.9, nesterov=True, decay=1e-6)
model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy', 'top_k_categorical_accuracy'])

while 1:
    try:
        im_location = input("Please enter location of image to be predicted...\n>>>")
        if im_location == 'e': break
        img = cv2.imread(im_location)/255.
        img = resize(img, (224, 224), mode='constant')
        img = np.reshape(img, (1, 224, 224, 3))
        prediction = model.predict(img)
        print(encode_prediction(prediction, 5))
        print("*"*20)
    except Exception as e:
        print("An error occured...")
        print(e)