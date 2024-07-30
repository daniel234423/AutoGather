import cv2
import pytesseract
import re
import numpy as np
import os
from .modelo import predict_image, color
from .model.queries import Info


#Fucnion principal (genera el video que quiero mostrar en la pagina web)
def Generate_Frame(video):
    vheiculo = []
    matriculasss = []   
    while True:
        ret, frame = video.read()
        #Variables necesarias
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.blur(gray, (3,3))
        canny = cv2.Canny(gray, 150, 200)
        cnt, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        placa = Generate_Matricula(frame, ret, gray, cnt)
        if placa == None:
            pass
        elif placa not in matriculasss:  
            img = cv2.imread('app/static/img/frame.jpg')
            matriculasss.append(placa)
            model = predict_image(img)
            model_color = color(img)
            print(matriculasss[-1])
            Info.post_all([matriculasss[-1]], model, model_color)
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        # Produce un marco de datos multipart/form-data con una imagen JPEG codificada
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n' )



            

def Generate_Matricula(frame, ret, gray, cnt):
    placas = []
    placa_format = r"^[A-Z]{3}-\d{3}$"
    placa_format_cl = r"^[A-Z]{2}\d{2}-[A-Z]{2}$"
    if not ret:pass
    x1, y1 = 100, 100
    x2, y2 = 700, 400
    x3, y3 = 300, 40
    x4, y4 = 700, 400
    roi2 = frame[y3:y4, x3:x4]
    roi = frame[y1:y2, x1:x2]
    #convertimos el area deseada a escala de grises
    for c in cnt:
        area = cv2.contourArea(c)
        #obtener los puntos x,y,w,h con boundingRect
        x,y,w,h = cv2.boundingRect(c)
        epsilon = 0.09*cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c ,epsilon, True)
        if len(approx) == 4 and area >= 2000 :
            cv2.imwrite(f'app/static/img/frame.jpg', roi2)
            aspect_ratio = float(w)/h
            if aspect_ratio >0.5 or aspect_ratio < 1:
                placa = gray[y:y+h, x:x+w]
                data = cv2.imread(f'frame0.jpg')
                datos = pytesseract.image_to_string(data,  config="--psm 11")
                cv2.imwrite(f'frame0.jpg', placa)
                if re.search(placa_format, datos) or re.search(placa_format_cl, datos):
                    if datos.strip() not in placas:
                        placas.append(datos.strip())
                        
                        
                        return(datos)

