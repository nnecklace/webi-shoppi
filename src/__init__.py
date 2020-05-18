from flask import Flask
app = Flask(__name__, template_folder='views')

from src.db import db
from src.models import products
from src import routes

try: 
    db.create_all()
except:
    pass