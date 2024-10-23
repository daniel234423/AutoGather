import re
import pytesseract
from ultralytics import YOLO
import cv2
import numpy 
model = YOLO('app/static/train3/weights/last.pt')
model2 = YOLO('/app/static/train3/weights/yolov8n.pt')
cap = cv2.VideoCapture('app/static/video/uni.mp4')



def get_matricula(video):
    while True:
        ret, frame = video.read()
        if not ret:pass
        results = model(frame)
        placas = []
        placa_format = r"^[A-Z0-9]{3}-\d{3}$"
        placa_format_cl = r"^[A-Z]{2}\d{4}-[A-Z]{2}$"
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                confidence = box.conf.item()
                if confidence > 0.5:
                    chosen_sector = frame[int(y1):int(y2), int(x1):int(x2)]
                    cv2.imwrite('frame.jpg', chosen_sector)
                    matricula = cv2.imread('frame.jpg')
                    datos = pytesseract.image_to_string(matricula,  config="--psm 11")
                    if re.search(placa_format, datos):
                        print(datos)
                        if datos.strip() not in placas:
                            placas.append(datos.strip())
                            print(placas)
            print(placas)
            cv2.imshow('Detección de Objetos', frame)
        if cv2.waitKey(1) & 0xFF  == ord('s'):
            break
    video.release()
    cv2.destroyAllWindows()


def get_car_frame(video):
    while True:
        ret, frame = video.read()
        if not ret:pass
        results = model2(frame)
        
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                confidence = box.conf.item()
                if confidence > 0.5:
                    chosen_sector = frame[int(y1):int(y2), int(x1):int(x2)]
                    cv2.imwrite('car_frame.jpg', chosen_sector)
                cv2.imshow('Detección de Objetos', frame)
        if cv2.waitKey(1) & 0xFF  == ord('s'):
            break
    video.release()
    cv2.destroyAllWindows()

get_car_frame(cap)