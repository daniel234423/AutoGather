
from keras.models import load_model
import numpy as np
import cv2 as cv

modeloConv2 = load_model('ModeloAuto.keras')

imagen = cv.imread('frame.jpg')
def predict_image(img):
    img = np.array(img).astype(float) / 255
    img = cv.resize(img, (224, 224))
    img = np.expand_dims(img, axis=0)
    pred = modeloConv2.predict(img)
    clase = np.argmax(pred[0])
    clases = ['camioneta', 'auto', 'moto']
    return clases[clase]

# Probar función de predicción
print(predict_image(imagen))