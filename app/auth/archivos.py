import cv2 as cv
import numpy as np
import os
from PIL import Image
import pytesseract

video1 = cv.VideoCapture("app/static/video/uni.mp4")        
rect_0=0
def primerCaptur():
    while True:
        ret1, frame1 = video1.read()

        if not ret1:break   
        x1, y1 = 100, 100
        x2, y2 = 700, 400
        roi = frame1[y1:y2, x1:x2]
        #convertimos el area deseada a escala de grises
        gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
        #mejorar la imagen con blur
        gray = cv.blur(gray,(3,3))
        #Aplicar derteccion de bordes con canny
        canny = cv.Canny(gray, 150,200)
        #encontrar los contornos 
        cnts, _ = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            area = cv.contourArea(c)
            #obtener los puntos x,y,w,h con boundingRect
            x,y,w,h = cv.boundingRect(c)
            epsilon = 0.09*cv.arcLength(c, True)
            approx = cv.approxPolyDP(c ,epsilon, True)
            if len(approx) == 4 and area > 1000:
                aspect_ratio = float(w)/h
                if aspect_ratio >0.5:
                    placa = gray[y:y+h, x:x+w]
                    cv.imshow("placa", placa)
                    number = 1
                    cv.imwrite(f'frame{number}.jpg', placa)
                    data = cv.imread(f'frame{number}.jpg')
                    
                    datos = pytesseract.image_to_string(data,  config="--psm 11")
                    print(datos)

        #cv.imshow("Video", frame1)
        cv.imshow("roi", roi)
        if cv.waitKey(5) & 0xFF == ord("s"):
            break
    video1.release()
    cv.destroyAllWindows()
    
primerCaptur()