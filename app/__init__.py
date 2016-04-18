from flask import Flask, request, redirect, url_for


UPLOAD_FOLDER ='stored_uploads/'

# this app is the variable holding the Flask instance
app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# this app is different, it is a package from which we import views
from app import views