import cv2
from .modelo import predict_image, Color
from .yolo_detect import get_matricula
from .model.queries import Info

# Función principal (genera el video que quiero mostrar en la página web)
def Generate_Frame(video, id_user):
    vheiculo = []
    matriculasss = []   
    while True:
        ret, frame = video.read()
        # Variables necesarias
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.blur(gray, (3,3))
        canny = cv2.Canny(gray, 150, 200)
        cnt, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        placa = get_matricula(frame, ret)
        
        if placa is None:
            pass
        elif placa and placa not in matriculasss:  
            matriculasss.append(placa)
            cv2.imwrite('app/static/img/hola.jpg', frame)
            img = cv2.imread('app/static/img/hola.jpg')
            model = predict_image(img)
            color = Color(img)
            print(model)
            print("patente", placa)
            Info.post_all(matriculasss[-1], model, color, id_user)
            
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        # Produce un marco de datos multipart/form-data con una imagen JPEG codificada
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

