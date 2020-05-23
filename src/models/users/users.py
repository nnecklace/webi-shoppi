from src.db import db
from sqlalchemy.dialects.postgresql import UUID
from src.constants import env_sqlite
import uuid

class User(db.Model):
    __tablename__ = "users"
    id_field = ""

    if not env_sqlite():
        id_field = UUID(as_uuid=True)
    else:
        id_field = db.Integer
    
    id = db.Column(id_field, primary_key=True, default=uuid.uuid4())
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    balance = db.Column(db.Integer) # money will be stored as cents
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True