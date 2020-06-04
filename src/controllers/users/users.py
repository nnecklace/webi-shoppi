from flask import request
from src.controllers import render
from src.models import User
from src.forms import UserForm

class UserController:
    @staticmethod
    def index(username):
        return render("users/main.html", user = User.query.filter_by(username = username).first(), user_form = UserForm())

    @staticmethod
    def update(username):
        user_form = UserForm(request.form)
        user = User.query.filter_by(username = username).first()

        if not user_form.validate():
            return render("users/main.html", user = user, user_form = user_form)

        if not user.update(user_form):
            return render("users/main.html", session_error = "Käyttäjätilin päivittäminen epäonnistui", user = user, user_form = user_form)

        return render("users/main.html", user = user, user_form = UserForm())
