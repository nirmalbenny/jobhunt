from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_simplemde import SimpleMDE
import os

#creaing an instance of the flask app------------------------------------
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
#Creating an instance of the Flask-Login-Manager
login = LoginManager(app) 


#telling flask about the config file we have created---------------------
app.config.from_object(Config)
SimpleMDE(app)
#Creating Sqlite database instance---------------------------------------
db = SQLAlchemy(app)

#Migrate engines instance------------------------------------------------
migrate = Migrate(app, db)



#importing our routes into the init file
from app import routes
from app import models

 