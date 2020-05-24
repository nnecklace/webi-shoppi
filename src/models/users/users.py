from src.db import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text, exc
from src.constants import env_sqlite
from src.encryption import encrypt, check_pwd
import sys

class User(db.Model):
    __tablename__ = "users"
    id_field = None

    if not env_sqlite():
        id_field = UUID(as_uuid=True)
    else:
        id_field = db.Integer
    
    id = db.Column(id_field, primary_key=True, server_default=text("uuid_generate_v4()"), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    balance = db.Column(db.Integer) # money will be stored as cents
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    products = db.relationship("Product", backref="users", lazy=True)

    def __init__(self, username, email, first_name, last_name, password):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = encrypt(password)
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def save(self):
        db.session().add(self)
        try:
            db.session().commit()
        except exc.SQLAlchemyError as err:
            print("[ERROR] user save : " + str(err), sys.stderr)
            return False

        print("[SUCCESS] user was created successfully")
        return True

    @staticmethod
    def findByUsernamePassword(username, password):
        user = User.query.filter_by(username = username).first()

        if not user:
            return None

        if check_pwd(user.password, password):
            return user

        return None
