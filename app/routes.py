from flask import render_template, Response, redirect, request, session
from .main import crear_app
from .model.queries import Info
from .archivos import Generate_Frame
from flask_bcrypt import Bcrypt
import cv2 as cv

app = crear_app()
bcrypt = Bcrypt(app)
video1 = None

@app.route("/")
def main():
    return render_template("index.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/app")
def aplicacion():
    info = Info.get_all()
    return render_template('app.html', info = info)
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login/register', methods = ['POST',])
def register():
    name_user = request.form['name']
    email = request.form['email']
    password = request.form['pass']
    errors = []

    if not name_user or len(name_user) < 3:
        errors.append("Nombre invalido")

    if not email or len(email) < 3:
        errors.append("email invalido")
    
    #ESTO SE USARA CUANDO SE LINKE LA BASE DE DATOS 
    #users = Usuario.select_by_email(email)
    #if len(users) > 0:
    #    errors.append("El usuario ya está registrado")

    if len(errors) > 0:
        return render_template("index.html", register_errors=errors)
    
    
    password = bcrypt.generate_password_hash(password).decode('utf-8')
    return redirect('/')

@app.route('/login/singin', methods = ['POST',])
def singin():
    name_user = request.form['name']
    email = request.form['email']
    password = request.form['pass']
    errors = []
    #ESTO SE USARA CUANDO ESTE LISTA EL ENLACE CON lA BASE DE DATOS 
    #user = Usuario.select_by_email(email)
    #if (len(user) != 1):
    #    errors.append("Email no registrado. Registrese por favor")
    #user = user[0]
    #if not bcrypt.check_password_hash(user.password,password):
    #    errors.append("El email y/o contraseña no corresponden")
    #if len(errors) > 0:
    #    return render_template("index.html", login_errors=errors)
    #session["id"] = user.id
    #session["nombre"] = f"{user.nombre} {user.apellido}"
    
    return redirect('/')

@app.route('/user')
def usuario():
    return render_template('user.html')

@app.route("/upload_video", methods=["POST"])
def upload_video():
    video_file = request.files["video"]
    video_path = "app/static/video/" + video_file.filename
    video_file.save(video_path)
    global video1
    video1 = cv.VideoCapture(video_path)
    return redirect('/')

@app.route("/video")
def video():
    return Response(Generate_Frame(video1), mimetype='multipart/x-mixed-replace; boundary=frame')
