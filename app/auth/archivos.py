import cv2 as cv
import pytesseract
import re



video1 = cv.VideoCapture("app/static/video/uni.mp4")        

def LicensePlateCapture():
    placas = []
    placa_format = r"^[A-Z]{3}-\d{3}$"
    placas_chile = r"^[A-Z]{2}-\d{3}-[A-Z]{2}$"
    number = 0
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
                if aspect_ratio >0.9:
                    placa = gray[y:y+h, x:x+w]
                    cv.imshow("placa", placa)
                    cv.imwrite(f'frame{number}.jpg', placa)
                    data = cv.imread(f'frame{number}.jpg')
                    datos = pytesseract.image_to_string(data,  config="--psm 11")
                    if re.search(placa_format, datos) and re.search(placas_chile, datos):
                        if datos.strip() not in placas:
                            placas.append(datos.strip())
                            print(placas)
        #cv.imshow("Video", frame1)
        cv.imshow("roi", roi)
        if cv.waitKey(30) & 0xFF == ord("s"):
            break
    video1.release()
    cv.destroyAllWindows()
    

LicensePlateCapture()

def DrawContornsAndVideo():
    while True:
        ret, frame = video1.read()
        if not ret:break
        else:
            ret, buffer = cv.imencode('.mp4', frame)
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            gray = cv.blur(gray, (3,3))
            canny = cv.Canny(gray, 150, 200)
            cnt, _ = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            for c in cnt:
                area = cv.contourArea(c)
                if area > 2000:
                    cv.drawContours(frame, [c],0,(0,255,0),2)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 
