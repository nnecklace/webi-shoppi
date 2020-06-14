from src.db import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text, exc
from src.constants import env_sqlite
import sys

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @staticmethod
    def generate_user_id_column():
        if not env_sqlite():
            return db.Column(UUID(as_uuid=True), server_default = text("uuid_generate_v4()"), primary_key=True, unique=True, nullable=False)
        else:
            return Base.id

    @staticmethod
    def get_user_id_field():
        if not env_sqlite():
            return UUID(as_uuid=True)
        else:
            return db.Integer

    def _commit(self, err_log):
        try:
            db.session().commit()
        except exc.SQLAlchemyError as err:
            print("[ERROR] " + err_log + " " + str(err), sys.stderr)
            return False

        return True

    def save(self, msg):
        db.session().add(self)
        return self._commit(msg)

    def delete(self, msg):
        db.session().delete(self)
        return self._commit(msg)