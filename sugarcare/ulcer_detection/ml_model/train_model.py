import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split

# Path to your dataset (original images or patches)
dataset_path = r'"C:\Users\Acer\Downloads\archive (3)\archive (3)\DFU\Patches'

# Function to load images
def load_data(dataset_path):
    images = []
    labels = []
    for label in ["Normal(Healthy skin)", "Abnormal(Ulcer)"]:
        folder_path = os.path.join(dataset_path, label)
        for image_name in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_name)
            image = cv2.imread(image_path)
            image = cv2.resize(image, (224, 224))  # Resize to 224x224 for training
            images.append(image)
            labels.append(0 if label == "Normal(Healthy skin)" else 1)  # Labels: 0 for normal, 1 for ulcer
    return np.array(images), np.array(labels)

# Load and prepare data
images, labels = load_data(dataset_path)
images = images / 255.0  # Normalize images

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=0.2, random_state=42)

# Data Augmentation
train_datagen = ImageDataGenerator(
    rotation_range=20, 
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator()

# Build the model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),  # Add Dropout layer to prevent overfitting
    Dense(1, activation='sigmoid')  # Output layer for binary classification (ulcer or non-ulcer)
])

# Compile the model
model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

# Early Stopping and Reduce Learning Rate on Plateau callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6)

# Train the model with data augmentation
history = model.fit(
    train_datagen.flow(X_train, y_train, batch_size=32),
    validation_data=val_datagen.flow(X_val, y_val, batch_size=32),
    epochs=50,
    callbacks=[early_stopping, lr_scheduler]
)

# Save the trained model
model.save(r'C:\Users\Acer\Downloads\Compressed\SugarCare_\SugarCare_\sugarcare\ulcer_detection\ml_model\foot_ulcer_model.h5')  # Save the model in the 'ml_model' directory

# Print the training and validation accuracies
train_accuracy = history.history['accuracy'][-1] * 100
val_accuracy = history.history['val_accuracy'][-1] * 100

print("Model training completed and saved.")
print(f"Training Accuracy: {train_accuracy:.2f}%")
print(f"Validation Accuracy: {val_accuracy:.2f}%")
