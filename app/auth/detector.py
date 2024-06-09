from PIL import Image
import requests
import io
from bs4 import BeautifulSoup
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range = 30,
    width_shift_range = 0.25,
    height_shift_range = 0.25,
    shear_range = 15,
    zoom_range = [0.5, 1.5],
    validation_split=0.2 #20% para pruebas
)
data_gen_entrenamiento = datagen.flow_from_directory('app/static/img/dataset', target_size=(224,224),
                                                    batch_size=32, shuffle=True, subset='training')
data_gen_pruebas = datagen.flow_from_directory('app/static/img/dataset', target_size=(224,224),
                                                    batch_size=32, shuffle=True, subset='validation')

#Imprimir 10 imagenes del generador de entrenamiento
for imagen, etiqueta in data_gen_entrenamiento:
    for i in range(10):
        plt.subplot(2,5,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(imagen[i])
    break
plt.show()



url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4"
mobilenetv2_layer = hub.KerasLayer(url, input_shape=(224, 224, 3), trainable=False)

modelo = tf.keras.Sequential([
    tf.keras.layers.Reshape((224, 224, 3)),  # Aseguramos que la entrada tenga la forma correcta
    tf.keras.layers.Lambda(lambda x: mobilenetv2_layer(x)),  # Envuelve la capa de TensorFlow Hub
    tf.keras.layers.Flatten(),  # Aplanamos la salida de mobilenetv2_layer
    tf.keras.layers.Dense(3, activation='softmax')
])
modelo.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
historial = modelo.fit(
    data_gen_entrenamiento, 
    epochs=50, 
    validation_data=data_gen_pruebas
)

modelo.summary()
def categorizar(url):
    respuesta = requests.get(url)
    soup = BeautifulSoup(respuesta.content, 'html.parser')

    # Find the img tag
    img_tag = soup.find('img')
    if img_tag is None:
        print("Error: Couldn't find img tag")
        return None

    img_url = img_tag['src']
    img_respuesta = requests.get(img_url)
    if img_respuesta.headers['Content-Type'].startswith('image/'):
        img = Image.open(io.BytesIO(img_respuesta.content))
        img = np.array(img).astype(float)/255
        img = cv2.resize(img, (224,224))
        prediccion = modelo.predict(img.reshape(-1, 224, 224, 3))
        return np.argmax(prediccion[0], axis=-1)
    else:
        print("Error: Not an image file")
        return None

url = 'https://www.mdzol.com/u/fotografias/m/2021/1/29/f1280x720-1012506_1144181_5050.jpg'
prediccion = categorizar(url)
if prediccion is not None:
    for x in prediccion:
        print(prediccion)