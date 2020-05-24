from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from os import urandom

app = Flask(__name__, template_folder='views')

app.config["SECRET_KEY"] = urandom(32)

from src.db import db
from src.models import products, users
from src import routes

"""
Login manager
"""
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_message = "This is login message" # remove?

@login_manager.user_loader
def load_user(user_id):
    return users.User.query.get(user_id)

"""
Password encryption
"""
crypto = Bcrypt(app)

def encrypt(str):
    return crypto.generate_password_hash(str, 13)

def check(candidate):
    return crypto.check_password_hash(encrypt(candidate), candidate)

try: 
    db.create_all()
except:
    pass
