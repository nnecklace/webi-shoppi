from functools import wraps
from flask_login import current_user
from flask import redirect, url_for
from src.models import User
from src import login_manager

def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not (current_user and current_user.is_authenticated):
            return login_manager.unauthorized()
        # Don't trust flask sessions or users
        # We could try and cache this value ?
        user = None

        if "username" in kwargs:
            user = User.query.filter_by(username = kwargs["username"]).first()
        else:
            user = User.query.get(kwargs["id"])

        if user == None or not user.get_id() == current_user.id:
            return login_manager.unauthorized()

        return fn(*args, **kwargs)
    
    return wrapper
