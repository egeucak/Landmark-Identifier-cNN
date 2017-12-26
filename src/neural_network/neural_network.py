from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.callbacks import EarlyStopping
import numpy as np
from keras.datasets import fashion_mnist
from keras.utils import np_utils

X_loc = "../feature_extractor/output2.npy"
Y_loc = "../feature_extractor/labels2.npy"

X = np.load(X_loc)
Y = np.load(Y_loc)

'''X = np.expand_dims(X, axis=2)
Y = Y.astype('float32')

(X, Y), (X_test, Y_test) = fashion_mnist.load_data()
X = X.reshape(-1, 28*28)
X = X.astype('float32')
X /= 255

Y = np_utils.to_categorical(Y, 10)'''

X /= np.max(X)

early_stopping = EarlyStopping(monitor='val_loss', patience=10)

print(X.shape)
print(Y.shape)

model = Sequential()
model.add(Dense(800, activation='relu', input_shape=X.shape[1:]))
model.add(Dense(400, activation='relu'))
#model.add(Dense(200, activation='relu'))
model.add(Dense(len(Y[0]), activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(X, Y, epochs=300,
          batch_size=32,
          validation_split=0.2,
          callbacks=[early_stopping], shuffle=True)

scores = model.evaluate(X,Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
model.save("model.h5")