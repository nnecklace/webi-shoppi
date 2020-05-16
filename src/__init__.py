from flask import Flask
app = Flask(__name__, template_folder='views')

from src.db import db
from src.models.products import products
from src import routes

db.create_all()