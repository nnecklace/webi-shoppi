from flask_sqlalchemy import SQLAlchemy
from src import app
from src.constants import env_production, env_sqlite, env_db_url

if not env_production():
    app.config["SQLALCHEMY_ECHO"] = True

app.config["SQLALCHEMY_DATABASE_URI"] = env_db_url()

db = SQLAlchemy(app)