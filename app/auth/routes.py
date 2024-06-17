from flask import Flask, render_template, Response
from .main import crear_app
from .archivos import DrawContornsAndVideo
import cv2 as cv
app = crear_app()

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/video")
def video():
    return Response(DrawContornsAndVideo(), mimetype='multipart/x-mixed-replace; boundary=frame')
