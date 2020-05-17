from flask_sqlalchemy import SQLAlchemy
from src import app

import os

if os.environ.get("ENV") == "HEROKU":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
elif os.environ.get("ENV") == "SQLITE":
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_ECHO"] = True
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://postgres@localhost:5432/webi_shoppi"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)