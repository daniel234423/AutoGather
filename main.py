from flask import Flask
from app.auth.routes import app

app = app
app.run(debug=True)