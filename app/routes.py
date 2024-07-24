from flask import render_template, Response, redirect
from .main import crear_app
from .archivos import Generate_Frame
import cv2 as cv
app = crear_app()
video1 = cv.VideoCapture("app/static/video/uni.mp4")        


@app.route("/")
def main():
    return render_template("index.html")
@app.route("/home")
def home():
    return redirect('/')
@app.route("/video")
def video():
    return Response(Generate_Frame(video1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/contact")
def contact():
    return render_template("contact.html")