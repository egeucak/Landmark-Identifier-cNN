from keras.applications.xception import Xception
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.xception import preprocess_input, decode_predictions
from keras.layers import Dense, GlobalAveragePooling2D, Dropout, Flatten, Reshape, AveragePooling2D, Convolution2D
from keras.layers import Input, MaxPooling2D
from keras.models import Model, Sequential
from keras.optimizers import Adamax
import numpy as np
import keras

import os
import glob

def get_nb_files(directory):
    """Get number of files by searching directory recursively"""
    if not os.path.exists(directory):
        return 0
    cnt = 0
    for r, dirs, files in os.walk(directory):
        for dr in dirs:
            cnt += len(glob.glob(os.path.join(r, dr + "/*")))
    return cnt

def main():
    #train_dir = "images"
    train_dir = '/home/ege/Desktop/machine learning/project/data/Yeni klasör TMM'

    train_dir = '/home/ege/Desktop/machine learning/project/data/images2/images_train'
    test_dir = '/home/ege/Desktop/machine learning/project/data/images2/images_test'

    train_dir = '/home/ege/Desktop/machine learning/project/data/mnist/mnist_png/training'
    test_dir = '/home/ege/Desktop/machine learning/project/data/mnist/mnist_png/testing'

    im_size = (100,100)

    nb_train_samples = get_nb_files(train_dir)
    nb_classes = len(glob.glob(train_dir + "/*"))
    nb_epoch = 200
    batch_size = 5

    train_datagen = ImageDataGenerator(
        rescale=1./255,
        #preprocessing_function=preprocess_input,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=im_size,
        batch_size=batch_size
    )

    test_generator = train_datagen.flow_from_directory(
        test_dir,
        target_size=im_size
    )

    sgd = Adamax(lr=0.001)
    '''model = Xception(weights='imagenet',
                     include_top=False,
                     input_shape=(150,150,3))

    for layer in model.layers[:-3]:
        layer.trainable = False'''

    #input = model.output
    input = Input(shape=(100,100,3))
    #x = Model(inputs=input, outputs=model.input)
    #x = GlobalAveragePooling2D()(input)
    #input2 = x.output
    print("-"*20)
    print(input)
    print("-" * 20)
    x = Convolution2D(32, (3,3), activation='relu')(input)
    x = Convolution2D(32, (3, 3), activation='relu')(x)
    x = MaxPooling2D(pool_size=(2,2))(x)
    x = Dropout(0.35)(x)

    x = Convolution2D(32, (3,3), activation='relu')(x)
    x = Convolution2D(32, (3, 3), activation='relu')(x)
    x = MaxPooling2D(pool_size=(2,2))(x)

    x = Flatten()(x)

    x = Dense(400, activation='relu')(x)
    x = Dropout(0.35)(x)

    #x = Dense(300, activation='relu')(x)
    #x = Dropout(0.3)(x)
    #x = Dense(len(target[0]), activation='relu')(x)
    predictions = Dense(nb_classes, activation='softmax')(x)
    model = Model(inputs=input, outputs=predictions)

    model.compile(loss='categorical_crossentropy',
                  optimizer=sgd,
                  metrics=['accuracy'])

    early_stop = keras.callbacks.EarlyStopping(monitor='acc',
                                               min_delta=0,
                                               patience=10,
                                               verbose=0,
                                               mode='auto'
                                               )
    check_point_file = "weights-checkpoint.hdf5"
    check_point = keras.callbacks.ModelCheckpoint(filepath=check_point_file,
                                                  monitor='val_acc',
                                                  verbose=1
                                                  )
    try:
        model.fit_generator(
            generator=train_generator,
            steps_per_epoch=nb_train_samples,
            epochs=nb_epoch,
            class_weight='auto',
            callbacks=[check_point],
            shuffle=True,
            use_multiprocessing=True,
            workers=100,
            validation_data=test_generator
        )
        model.save("model.h5")
    except KeyboardInterrupt:
        model.save("model.h5")

main()