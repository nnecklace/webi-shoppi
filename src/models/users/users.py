from src.db import db
from src.models import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text, exc
from src.constants import env_sqlite
from src.encryption import encrypt, check_pwd
import sys

class User(Base):
    __tablename__ = "users"

    if not env_sqlite():
        id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"), unique=True, nullable=False)
    
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    balance = db.Column(db.Integer, default=0) # money will be stored as cents
    
    products = db.relationship("Product", back_populates="user")

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

    def _commit(self, err_log = "", succ_log = ""):
        try:
            db.session().commit()
        except exc.SQLAlchemyError as err:
            print("[ERROR] " + err_log + " " + str(err), sys.stderr)
            return False

        if succ_log:
            print("[SUCCESS] " + succ_log)

        return True

    def save(self):
        db.session().add(self)
        return self._commit("user create:")

    def update(self, user_form):
        self.username = user_form.username.data
        self.email = user_form.email.data
        self.first_name = user_form.first_name.data
        self.last_name = user_form.last_name.data
        return self._commit("user update:")

    def update_password(self, password):
        self.password = encrypt(password)
        return self._commit("user password:")

    @staticmethod
    def find_by_username_password(username, password):
        user = User.query.filter_by(username = username).first()

        if not user:
            return None

        if check_pwd(user.password, password):
            return user

        return None
