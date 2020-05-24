from src import app
from flask_bcrypt import Bcrypt

"""
Password encryption
"""
crypto = Bcrypt(app)

def encrypt(str):
    return crypto.generate_password_hash(str, 13).decode("utf-8")

def check_pwd(hash_str, candidate):
    return crypto.check_password_hash(hash_str, candidate)
