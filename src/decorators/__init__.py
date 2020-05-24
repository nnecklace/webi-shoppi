from functools import wraps
from flask_login import current_user
from flask import redirect, url_for
from src.models.users import User

def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Don't trust flask sessions or users
        # We could try and cache this value ?
        user = User.query.filter_by(username = kwargs["username"]).first()
        if not user.id == current_user.id:
            return redirect(url_for('index'))

        return fn(*args, **kwargs)
    
    return wrapper

