from functools import wraps
from flask_login import current_user
from flask import redirect, url_for
from src.models import User

def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Don't trust flask sessions or users
        # We could try and cache this value ?
        user = None

        if "username" in kwargs:
            user = User.query.filter_by(username = kwargs["username"]).first()
        else:
            user = User.query.get(kwargs["id"])

        if user == None or not user.id == current_user.id:
            return redirect(url_for('index'))

        return fn(*args, **kwargs)
    
    return wrapper

