import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import cv2 as cv
train_dir = 'app/static/dataset'
test_dir = 'app/static/dataset'

# Crear generador de imágenes con augmentation
datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=30,
    width_shift_range=0.25,
    height_shift_range=0.25,
    shear_range=15,
    zoom_range=[0.5, 1.5],
    validation_split=0.2  # 20% para pruebas
)

# Crear generadores de entrenamiento y prueba
data_gen_entrenamiento = datagen.flow_from_directory(train_dir, target_size=(224, 224),
                                                    batch_size=32, shuffle=True, subset='training')
data_gen_pruebas = datagen.flow_from_directory(train_dir, target_size=(224, 224),
                                                    batch_size=32, shuffle=True, subset='validation')

# Crear modelo de clasificación
modeloConv2 = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(512, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(1024, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(2048, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(1000, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

# Compilar modelo
modeloConv2.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entrenar modelo
modeloConv2.fit(data_gen_entrenamiento, epochs=50, batch_size=32, validation_data=data_gen_pruebas)

modeloConv2.save("ModeloAuto.keras")