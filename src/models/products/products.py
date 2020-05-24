from src.db import db
from sqlalchemy.dialects.postgresql import UUID
from src.constants import env_sqlite
from sqlalchemy import exc
import sys

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)


    id_field = None
    if not env_sqlite():
        id_field = UUID(as_uuid=True)
    else:
        id_field = db.Integer

    user_id = db.Column(id_field, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, name, price, quantity, user_id):
        self.name = name
        self.price = price # TODO: convert to cents
        self.quantity = quantity
        self.user_id = user_id

    def _commit(self, err_log):
        try:
            db.session().commit()
        except exc.SQLAlchemyError as err:
            print("[ERROR] " + err_log + " " + str(err), sys.stderr)
            return False

        return True

    def save(self):
        db.session().add(self)
        return self._commit("product create:")

    def update(self):
        return self._commit("product " + str(self.id) + " update :")
    
    def delete(self):
        db.session().delete(self)
        return self._commit("product " + str(self.id) + " delete :")
