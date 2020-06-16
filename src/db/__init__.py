from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from src import app
from src.constants import env_production, env_sqlite, env_db_url

if not env_production():
    app.config["SQLALCHEMY_ECHO"] = True

app.config["SQLALCHEMY_DATABASE_URI"] = env_db_url()

db = SQLAlchemy(app)

if env_sqlite():
    def _fk_pragma_on_connect(dbapi_con, con_record):
        dbapi_con.execute('pragma foreign_keys=ON')

    with app.app_context():
        event.listen(db.engine, 'connect', _fk_pragma_on_connect)