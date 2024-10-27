from flask import render_template, Response, redirect, request, session
from .main import crear_app
from .model.queries import Info
from .archivos import Generate_Frame
from flask_bcrypt import Bcrypt
import cv2 as cv
from .model.usuarios import Users

app = crear_app()
bcrypt = Bcrypt(app)
video1 = None

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/play_app")
def aplicacion():
    info = Info.get_all()
    return render_template('app.html', info=info)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/register', methods=['POST'])
def register():
    name_user = request.form['name']
    email = request.form['email']
    password = request.form['pass']
    print(password)
    errors = []

    if not name_user or len(name_user) < 3:
        errors.append("Nombre inválido")
    if not email or len(email) < 3:
        errors.append("Email inválido")
    if Users.login_by_email(email):
        errors.append("El usuario ya está registrado")

    if len(errors) > 0:
        return render_template("index.html", register_errors=errors)
    password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = Users.user_register(name_user, email, password)
    return redirect('/')

@app.route('/login/singin', methods=['POST'])
def singin():
    email = request.form['email']
    password = request.form['password'].strip()
    errors = []
    user = Users.login_by_email(email)
    
    print(f"Email ingresado: {email}")
    print(f"Contraseña ingresada: {password}") 
    
    if not user or len(user) != 1:
        errors.append("Email no registrado. Registrese por favor.")
    else:
        user = user[0]
        print(f"Contraseña de Base de datos: {user.password}",)
        print(bcrypt.check_password_hash(user.password,password))
    if not bcrypt.check_password_hash(user.password,password):
        errors.append("El email y/o contraseña no corresponden")
    session["id"] = user.id
    session["nombre"] = user.name
    print(f"{session["nombre"]}")


    return redirect('/')

@app.route('/iniciar_sesion')
def iniciar_sesion():
    return render_template('iniciar-sesion.html')

@app.route('/user')
def usuario():
    return render_template('user.html')

@app.route("/upload_video", methods=["POST"])
def upload_video():
    video_file = request.files["video"]
    video_path = "app/static/video" + video_file.filename
    video_file.save(video_path)
    global video1
    video1 = cv.VideoCapture(video_path)
    return redirect('/play_app')

@app.route("/video")
def video():
    return Response(Generate_Frame(video1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/")
def main():
    return render_template("index.html")