from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.callbacks import EarlyStopping
import numpy as np

X_loc = "../feature_extractor/output.npy"
Y_loc = "../feature_extractor/labels.npy"

X = np.load(X_loc)
Y = np.load(Y_loc)

early_stopping = EarlyStopping(monitor='val_loss', patience=10)

print(len(X))

model = Sequential()
model.add(Dense(1500, input_dim=len(X[0]), activation='relu'))
model.add(Dense(600, activation='relu'))
model.add(Dense(len(Y[0])))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, Y, epochs=300,
          batch_size=400,
          validation_split=0.2,
          callbacks=[early_stopping], shuffle=True)

scores = model.evaluate(X,Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
model.save("model.h5")