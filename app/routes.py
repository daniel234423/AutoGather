from flask import render_template, Response, redirect, request
from .main import crear_app
from .model.queries import Info
from .archivos import Generate_Frame
import cv2 as cv

app = crear_app()
video1 = None

@app.route("/")
def main():
    info = Info.get_all()
    return render_template("index.html", info=info)

@app.route("/home")
def home():
    return redirect('/')

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

@app.route("/contact")
def contact():
    return render_template("contact.html")