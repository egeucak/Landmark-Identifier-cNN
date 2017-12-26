from keras.applications.xception import Xception
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.xception import preprocess_input, decode_predictions
from keras.layers import Dense, GlobalAveragePooling2D, Dropout, Flatten, Reshape
from keras.models import Model
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
    nb_train_samples = get_nb_files(train_dir)
    nb_classes = len(glob.glob(train_dir + "/*"))
    nb_epoch = 200
    batch_size = 50

    train_datagen = ImageDataGenerator(
        rescale=1./255,
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
        target_size=(40,40),
        batch_size=batch_size
    )


    output_file = "labels.npy"
    target = np.load(output_file)

    sgd = Adamax(lr=0.006)
    model = Xception(weights='imagenet',
                     include_top=False)

    for layer in model.layers:
        layer.trainable = False

    print(model.layers[-1])
    output_features = model.layers[-1].output
    print("----------------")
    print(output_features)
    print("----------------")
    predictions = Dense(nb_classes, activation='softmax')(model.output)
    model = Model(inputs=model.input, outputs=predictions)

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
            callbacks=[early_stop, check_point],
            shuffle=True
        )
        model.save("model.h5")
    except KeyboardInterrupt:
        model.save("model.h5")

main()