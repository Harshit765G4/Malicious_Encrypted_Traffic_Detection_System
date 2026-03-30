from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense

def create_gru(input_shape, num_classes):

    model = Sequential()

    model.add(GRU(64, input_shape=input_shape))

    model.add(Dense(64, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model