

import numpy as np
import tensorflow as tf
from tensorflow import keras

# Directorios de entrenamiento y prueba
train_dir = 'app/static/dataset_color'
# Crear generador de imágenes con augmentation
datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=10,  # Menos rotación para evitar distorsiones
    width_shift_range=0.1,  # Menos desplazamiento
    height_shift_range=0.1,
    shear_range=5,  # Menos cizallamiento
    zoom_range=[0.8, 1.2],  # Rango de zoom más reducido
    validation_split=0.2
)

# Crear generadores de entrenamiento y prueba
data_gen_entrenamiento = datagen.flow_from_directory(train_dir, target_size=(240, 240),  # Tamaño de imagen reducido
                                                    batch_size=64,  # Aumentar tamaño de batch
                                                    shuffle=True, 
                                                    subset='training')
data_gen_pruebas = datagen.flow_from_directory(train_dir, target_size=(240, 240),
                                                batch_size=64, 
                                                shuffle=True, 
                                                subset='validation')

# Crear modelo de clasificación más simple
modeloConv2 = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(240, 240, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Dropout(0.3),  # Menos Dropout
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(5, activation='softmax')
])

# Compilar modelo
modeloConv2.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entrenar modelo
modeloConv2.fit(data_gen_entrenamiento, epochs=20, validation_data=data_gen_pruebas)  # Reducir épocas

modeloConv2.save("ModeloColores.keras")