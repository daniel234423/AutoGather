import cv2
import pytesseract
import re
import numpy as np




#Fucnion principal (genera el video que quiero mostrar en la pagina web)
def Generate_Frame(video):


    matriculasss = []   
    while True:
        ret, frame = video.read()
        #Variables necesarias
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.blur(gray, (3,3))
        canny = cv2.Canny(gray, 150, 200)
        cnt, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        Add_Contour(frame, ret, cnt)
        matriculas = Generate_Matricula(frame, ret, gray, cnt)
        if matriculas == None:
            pass
        elif matriculas not in matriculasss:  
            matriculasss.append(matriculas)
            print(matriculasss)
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        # Produce un marco de datos multipart/form-data con una imagen JPEG codificada
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n' )


#Funcion para agregar contornos dentro de el video en la pagina web
def Add_Contour(frame, ret, cnt):
    for c in cnt:
        area = cv2.contourArea(c)
        epsilon = 0.09*cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        if len(approx) == 4 and area >= 700:
            cv2.drawContours(frame, [c], 0, (0,0,255), 4)
            
            

def Generate_Matricula(frame, ret, gray, cnt):
    placas = []
    placa_format = r"^[A-Z]{3}-\d{3}$"
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
        if len(approx) == 4 and area >= 3000:
            aspect_ratio = float(w)/h
            if aspect_ratio >0.7:
                placa = gray[y:y+h, x:x+w]
                cv2.imwrite(f'frame0.jpg', placa)
                data = cv2.imread(f'frame0.jpg')
                datos = pytesseract.image_to_string(data,  config="--psm 11")
                if re.search(placa_format, datos):
                    if datos.strip() not in placas:
                        placas.append(datos.strip())
                        return(placas)
# Función para detectar colores específicos
def Generate_color():
    #video1 = cv2.VideoCapture(0)        
    black_matte_high = np.array([180, 255, 50], np.uint8)
    black_matte_low = np.array([0, 0, 0], np.uint8)
    gray_high = np.array([180, 50, 150], np.uint8)
    gray_low = np.array([0, 0, 100], np.uint8)
    white_high = np.array([180, 50, 255], np.uint8)
    white_low = np.array([0, 0, 200], np.uint8)
    red_high = np.array([10, 255, 255], np.uint8)
    red_low = np.array([0, 100, 100], np.uint8)
    bluebajo1 = np.array([100,100,20],np.uint8)

    bluelto1 = np.array([125,255,255],np.uint8)


    while True:
        ret, frame = video1.read()
        if not ret:break
            # Convertir la imagen a HSV (Hue, Saturation, Value)
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_black = cv2.inRange(frameHSV,black_matte_high,black_matte_low)
        mask_gris = cv2.inRange(frameHSV,gray_high,gray_low)
        mask_blanco = cv2.inRange(frameHSV,white_high,white_low)
        mask_rojo = cv2.inRange(frameHSV,red_high,red_low)
        mask_blue = cv2.inRange(frameHSV,bluebajo1,bluelto1)
        #agregar contorno
        contornos_negros , _ = cv2.findContours(mask_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contornos_blanco , _ = cv2.findContours(mask_blanco, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contornos_gris , _ = cv2.findContours(mask_gris, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contornos_rojo , _ = cv2.findContours(mask_rojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contornos_azul , _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contornos_negros:
            area = cv2.contourArea(c)
            if area > 3000:
                    #cordenadas de linea 22 a 29
                    M = cv2.moments(c)
                    if (M["m00"]==0): M["m00"]=1
                    x = int(M["m10"]/M["m00"])
                    y = int(M["m01"]/M["m00"])
                    cv2.circle(frame,(x,y),7,(0,0,0),-1)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame,'negro'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
                    nuevoContorno = cv2.convexHull(c)
                    cv2.drawContours(frame, [nuevoContorno] , 0,(0,0,0),2)
        for c in contornos_blanco:
            area = cv2.contourArea(c)
            if area > 3000:
                    #cordenadas de linea 22 a 29
                    M = cv2.moments(c)
                    if (M["m00"]==0): M["m00"]=1
                    x = int(M["m10"]/M["m00"])
                    y = int(M["m01"]/M["m00"])
                    cv2.circle(frame,(x,y),7,(255,255,255),-1)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame,'Blanco'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
                    nuevoContorno = cv2.convexHull(c)
                    cv2.drawContours(frame, [nuevoContorno] , 0,(255,255,255),2)
        for c in contornos_gris:
            area = cv2.contourArea(c)
            if area > 3000:
                    #cordenadas de linea 22 a 29
                    M = cv2.moments(c)
                    if (M["m00"]==0): M["m00"]=1
                    x = int(M["m10"]/M["m00"])
                    y = int(M["m01"]/M["m00"])
                    cv2.circle(frame,(x,y),7,(100, 100, 100),-1)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame,'Gris'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
                    nuevoContorno = cv2.convexHull(c)
                    cv2.drawContours(frame, [nuevoContorno] , 0,(100, 100, 100),2)
        for c in contornos_rojo:
            area = cv2.contourArea(c)
            if area > 3000:
                    #cordenadas de linea 22 a 29
                    M = cv2.moments(c)
                    if (M["m00"]==0): M["m00"]=1
                    x = int(M["m10"]/M["m00"])
                    y = int(M["m01"]/M["m00"])
                    cv2.circle(frame,(x,y),7,(255, 0, 0),-1)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame,'Rojo'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
                    nuevoContorno = cv2.convexHull(c)
                    cv2.drawContours(frame, [nuevoContorno] , 0,(255, 0, 0),2)
        for c in contornos_azul:
            area = cv2.contourArea(c)
            if area > 3000:
                    #cordenadas de linea 22 a 29
                    M = cv2.moments(c)
                    if (M["m00"]==0): M["m00"]=1
                    x = int(M["m10"]/M["m00"])
                    y = int(M["m01"]/M["m00"])
                    cv2.circle(frame,(x,y),7,(255, 0, 0),-1)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame,'Azul'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
                    nuevoContorno = cv2.convexHull(c)
                    cv2.drawContours(frame, [nuevoContorno] , 0,(255, 0, 0  ),2)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
    video1.release()
    cv2.destroyAllWindows()
    