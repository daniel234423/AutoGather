import cv2
import pytesseract
import re
import numpy as np
from .deteccion_colores import detectar_azul, detectar_blanco,  detectar_rojo, detectar_negro
from .modelo import predict_image
from .model.queries import Tarea


#Fucnion principal (genera el video que quiero mostrar en la pagina web)
def Generate_Frame(video):
    img = cv2.imread('app/static/img/frame.jpg')
    vheiculo = []
    matriculasss = []   
    while True:
        ret, frame = video.read()
        #Variables necesarias
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.blur(gray, (3,3))
        canny = cv2.Canny(gray, 150, 200)
        cnt, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        Add_Contour(frame, ret, cnt)
        Genrtae_colors(frame)
        placa = Generate_Matricula(frame, ret, gray, cnt)
        if placa == None:
            pass
        elif placa not in matriculasss:  
            matriculasss.append(placa)
            model = predict_image(img)
            for i in matriculasss:
                #Tarea.post_all(i, model, )
                print(model)
                print(i)
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        # Produce un marco de datos multipart/form-data con una imagen JPEG codificada
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n' )


#Funcion para agregar contornos dentro de el video en la pagina web
def Add_Contour(frame, ret, cnt):
    for c in cnt:
        area = cv2.contourArea(c)
        epsilon = 0.09*cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        if len(approx) == 4 and area >= 3000:
            cv2.drawContours(frame, [c], 0, (0,0,255), 4)
            cv2.imwrite(f'app/static/img/frame.jpg', frame)
            

def Generate_Matricula(frame, ret, gray, cnt):
    placas = []
    placa_format = r"^[A-Z]{3}-\d{3}$"
    placa_format_cl = r"^[A-Z]{2}\d{2}-[A-Z]{2}$"
    if not ret:pass
    x1, y1 = 100, 100
    x2, y2 = 700, 400
    roi = frame[y1:y2, x1:x2]
    #convertimos el area deseada a escala de grises
    for c in cnt:
        area = cv2.contourArea(c)
        #obtener los puntos x,y,w,h con boundingRect
        x,y,w,h = cv2.boundingRect(c)
        epsilon = 0.09*cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c ,epsilon, True)
        if len(approx) == 4 and area >= 2000 :
            cv2.drawContours(frame, [c], 0, (0,0,255), 4)
            aspect_ratio = float(w)/h
            if aspect_ratio >0.5 or aspect_ratio < 1:
                placa = gray[y:y+h, x:x+w]
                data = cv2.imread(f'frame0.jpg')
                datos = pytesseract.image_to_string(data,  config="--psm 11")
                cv2.imwrite(f'frame0.jpg', placa)
                if re.search(placa_format, datos) or re.search(placa_format_cl, datos):
                    if datos.strip() not in placas:
                        placas.append(datos.strip())
                        return(placas)
# Función para detectar colores específicos
def Genrtae_colors(frame):
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    detectar_azul(frame, frameHSV)
    detectar_blanco(frame, frameHSV)
    #detectar_gris(frame, frameHSV)
    detectar_negro(frame, frameHSV)
    detectar_rojo(frame, frameHSV)