import cv2
import numpy as np
# Definir los rangos de color en HSV
blanco_low = np.array([0, 0, 230])
blanco_high = np.array([180, 20, 255])


rojo_low = np.array([0, 150, 100])
rojo_high = np.array([10, 255, 255])

azul_low = np.array([100, 100, 100])
azul_high = np.array([120, 255, 255])

gris_low = np.array([0, 0, 100])
gris_high = np.array([180, 50, 200])

negro_low = np.array([0, 0, 0])
negro_high = np.array([180, 50, 100])


#AZUL
def detectar_azul(frame, frameHSV):
    mask_blue = cv2.inRange(frameHSV,azul_low,azul_high)
    contornos_azul , _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos_azul:
        area = cv2.contourArea(c)
        if area >= 5000:
            M = cv2.moments(c)
            if (M["m00"]==0): M["m00"]=1
            x = int(M["m10"]/M["m00"])
            y = int(M["m01"]/M["m00"])
            cv2.circle(frame,(x,y),7,(255, 0, 0),-1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,'Azul'.format(x,y),(x+10,y), font, 0.75,(255, 0, 0),1,cv2.LINE_AA)
            nuevoContorno = cv2.convexHull(c)
            cv2.drawContours(frame, [nuevoContorno] , 0,(255, 0, 0),2)



#NEGRO
def detectar_negro(frame, frameHSV):
    mask_black = cv2.inRange(frameHSV,negro_low,negro_high)
    contornos_negros , _ = cv2.findContours(mask_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos_negros:
        area = cv2.contourArea(c)
        if area >= 5000:
            M = cv2.moments(c)
            if (M["m00"]==0): M["m00"]=1
            x = int(M["m10"]/M["m00"])
            y = int(M["m01"]/M["m00"])
            cv2.circle(frame,(x,y),7,(0, 0, 0),-1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,'Negro'.format(x,y),(x+10,y), font, 0.75,(0, 0, 0),1,cv2.LINE_AA)
            nuevoContorno = cv2.convexHull(c)
            cv2.drawContours(frame, [nuevoContorno] , 0,(0, 0, 0),2)


#ROJO
def detectar_rojo(frame, frameHSV):
    mask_rojo = cv2.inRange(frameHSV,rojo_low,rojo_high)
    contornos_rojo, _ = cv2.findContours(mask_rojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos_rojo:
        area = cv2.contourArea(c)
        if area >= 5000:
            M = cv2.moments(c)
            if (M["m00"]==0): M["m00"]=1
            x = int(M["m10"]/M["m00"])
            y = int(M["m01"]/M["m00"])
            cv2.circle(frame,(x,y),7,(0, 0, 255),-1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,'Rojo',(x+10,y), font, 0.75,(0, 0, 255),1,cv2.LINE_AA)
            nuevoContorno = cv2.convexHull(c)
            cv2.drawContours(frame, [nuevoContorno], 0,(0, 0, 255),2)



#BLANCO
def detectar_blanco(frame, frameHSV):
    mask_blanco = cv2.inRange(frameHSV,blanco_low,blanco_high)
    contornos_blanco , _ = cv2.findContours(mask_blanco, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos_blanco:
        area = cv2.contourArea(c)
        if area >= 5000:
            M = cv2.moments(c)
            if (M["m00"]==0): M["m00"]=1
            x = int(M["m10"]/M["m00"])
            y = int(M["m01"]/M["m00"])
            cv2.circle(frame,(x,y),7,(255,255,255),-1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,'Blanco',(x+10,y), font, 0.75,(255,255,255),1,cv2.LINE_AA)
            nuevoContorno = cv2.convexHull(c)
            cv2.drawContours(frame, [nuevoContorno] , 0,(255,255,255),2)
            
#GRIS
def detectar_gris(frame, frameHSV):
    mask_gris = cv2.inRange(frameHSV,gris_low,gris_high)
    contornos_gris , _ = cv2.findContours(mask_gris, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos_gris:
        area = cv2.contourArea(c)
        if area >= 5000:
            M = cv2.moments(c)
            if (M["m00"]==0): M["m00"]=1
            x = int(M["m10"]/M["m00"])
            y = int(M["m01"]/M["m00"])
            cv2.circle(frame,(x,y),7,(128,128,128),-1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,'Gris',(x+10,y), font, 0.75,(128,128,128),1,cv2.LINE_AA)
            nuevoContorno = cv2.convexHull(c)
            cv2.drawContours(frame, [nuevoContorno] , 0,(128,128,128),2)