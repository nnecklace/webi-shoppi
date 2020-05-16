from flask_sqlalchemy import SQLAlchemy
from src import app

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://postgres@localhost:5432/webi_shoppi"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)