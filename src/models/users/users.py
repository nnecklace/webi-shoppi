from src.db import db
from src.models import Base, Product, CategoryProduct
from src.constants import get_max_integer, env_sqlite
from src.encryption import encrypt, check_pwd

class User(Base):
    __tablename__ = "users"

    id = Base.generate_user_id_column()
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    balance = db.Column(db.Integer, default=0) # money will be stored as cents
    
    products = db.relationship("Product", back_populates="user", passive_deletes=True)

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

    def update(self, user_form):
        self.username = user_form.username.data
        self.email = user_form.email.data
        self.first_name = user_form.first_name.data
        self.last_name = user_form.last_name.data
        return self._commit("user update:")

    def update_password(self, password):
        self.password = encrypt(password)
        return self._commit("user password:")

    def set_balance(self, balance):
        new_balance = self.balance + balance

        if new_balance > get_max_integer():
            new_balance = get_max_integer()

        self.balance = new_balance

        return self._commit("user balance:")

    def purchase(self, product):
        if product.quantity < 1:
            return False

        if product.user_id == self.id:
            return False

        if self.balance >= product.price:
            self.balance -= product.price
            product.user.set_balance(product.price)
            product.quantity -= 1
            return self._commit("user purchase product " + str(product.id) + ":")

        return False

    @staticmethod
    def find_by_username_password(username, password):
        user = User.query.filter_by(username = username).first()

        if not user:
            return None

        if check_pwd(user.password, password):
            return user

        return None
