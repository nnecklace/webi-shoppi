from src.db import db
from sqlalchemy.dialects.postgresql import UUID
from src.constants import env_sqlite

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @staticmethod
    def generate_user_id_field():
        if not env_sqlite():
            return UUID(as_uuid=True)
        else:
            return db.Integer

    @staticmethod
    def get_user_id_default():
        if not env_sqlite():
            return "uuid_generate_v4()"
        else:
            return "0"
