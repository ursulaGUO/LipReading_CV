import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import os

# --- Hyperparameters ---
BATCH_SIZE = 8
NUM_CLASSES = 10  # Example: 10 different action classes
SEQUENCE_LENGTH = 16  # Number of frames per video clip
IMAGE_SIZE = 128      # Resize frames to this size
LEARNING_RATE = 0.001
NUM_EPOCHS = 10

# --- Dummy Data Generator (Replace with your actual data loading) ---
def generate_dummy_data(num_samples, sequence_length, image_size, num_classes):
    X = np.random.rand(num_samples, sequence_length, image_size, image_size, 3).astype(np.float32)
    y = np.random.randint(0, num_classes, size=(num_samples,)).astype(np.int32)
    return X, tf.keras.utils.to_categorical(y, num_classes)

# --- 3D Convolutional Network Model ---
def create_3d_cnn_model(input_shape, num_classes):
    model = keras.Sequential(
        [
            layers.Conv3D(32, (3, 3, 3), activation="relu", input_shape=input_shape, padding="same"),
            layers.MaxPooling3D((1, 2, 2)),
            layers.Conv3D(64, (3, 3, 3), activation="relu", padding="same"),
            layers.MaxPooling3D((2, 2, 2)),
            layers.Conv3D(128, (3, 3, 3), activation="relu", padding="same"),
            layers.Conv3D(128, (3, 3, 3), activation="relu", padding="same"),
            layers.MaxPooling3D((2, 2, 2)),
            layers.Conv3D(256, (3, 3, 3), activation="relu", padding="same"),
            layers.Conv3D(256, (3, 3, 3), activation="relu", padding="same"),
            layers.MaxPooling3D((2, 2, 2)),
            layers.GlobalAveragePooling3D(),
            layers.Dense(num_classes, activation="softmax"),
        ]
    )
    return model

if __name__ == '__main__':
    # --- Data Preparation (Replace with your actual data loading) ---
    NUM_SAMPLES = 100  # Number of dummy video samples
    INPUT_SHAPE = (SEQUENCE_LENGTH, IMAGE_SIZE, IMAGE_SIZE, 3)
    X_train, y_train = generate_dummy_data(NUM_SAMPLES, SEQUENCE_LENGTH, IMAGE_SIZE, NUM_CLASSES)
    X_val, y_val = generate_dummy_data(NUM_SAMPLES // 2, SEQUENCE_LENGTH, IMAGE_SIZE, NUM_CLASSES)

    # Create the 3D CNN model
    model = create_3d_cnn_model(INPUT_SHAPE, NUM_CLASSES)

    # Compile the model
    optimizer = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)
    model.compile(optimizer=optimizer, loss="categorical_crossentropy", metrics=["accuracy"])

    # Print the model summary
    model.summary()

    # --- Training ---
    print("\n--- Training ---")
    history = model.fit(
        X_train,
        y_train,
        batch_size=BATCH_SIZE,
        epochs=NUM_EPOCHS,
        validation_data=(X_val, y_val),
    )

    # --- Evaluation (Optional) ---
    print("\n--- Evaluation ---")
    loss, accuracy = model.evaluate(X_val, y_val, verbose=0)
    print(f"Validation Loss: {loss:.4f}")
    print(f"Validation Accuracy: {accuracy:.4f}")