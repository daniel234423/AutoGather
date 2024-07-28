
from keras.models import load_model
import numpy as np
import cv2 as cv
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

modeloConv2 = load_model(r'app\model\ModeloAuto.keras', compile=False)


def predict_image(img):
    img = np.array(img).astype(float) / 255
    img = cv.resize(img, (224, 224))
    img = np.expand_dims(img, axis=0)
    pred = modeloConv2.predict(img)
    clase = np.argmax(pred[0])
    clases = ['camioneta', 'auto', 'moto']
    return clases[clase]