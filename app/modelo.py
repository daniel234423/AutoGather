
from keras.models import load_model
import numpy as np
import cv2 as cv
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

modeloConv2 = load_model(r'app\model\ModeloAuto.keras', compile=False)
modeloConv2color = load_model(r'app\model\ModeloColores.keras', compile=False)
img = cv.imread('app/static/img/negro.jpg')

def predict_image(img):
    img = np.array(img).astype(float) / 255
    img = cv.resize(img, (224, 224))
    img = np.expand_dims(img, axis=0)
    pred = modeloConv2.predict(img)
    clase = np.argmax(pred[0])
    clases = ['camioneta', 'auto', 'moto']
    return clases[clase]

def color(img):
    img = np.array(img).astype(float) / 255
    img = cv.resize(img, (224, 224))
    img = np.expand_dims(img, axis=0)
    pred = modeloConv2color.predict(img)
    clase = np.argmax(pred[0])
    clases = ['rojo', 'blanco', 'gris', 'negro', 'azul']
    return clases[clase]
