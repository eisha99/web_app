
from flask_sqlalchemy import SQLAlchemy
import os 
from flask import Flask
import secrets 
# initiate flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex() # secret key to enable sessions
# connect the app to the database
path = os.path.join(os.path.dirname(__file__), 'database.db') # to ensure that works on any machine (with any folder setup)
URI = 'sqlite:///{}'.format(path) 
app.config['SQLALCHEMY_DATABASE_URI'] = URI # later switch to: #s.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
db = SQLAlchemy(app)

# import the routing file
from app import routing
