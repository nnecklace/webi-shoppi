from flask import request, redirect, url_for
from flask_login import login_user, logout_user
from src.controllers.base import render
from src.models.users import User
from src.forms.authentication import RegisterForm, LoginForm
from src.db import db


class AuthenticationController:
    @staticmethod
    def register_form():
        return render("authentication/register.html", form = RegisterForm())

    @staticmethod
    def register():
        form = RegisterForm(request.form)

        if not form.validate():
            return render("authentication/register.html", form = form)

        return render("index.html")

    @staticmethod
    def login():
        login_form = LoginForm(request.form)

        if not login_form.validate():
            return render(login_form.view_data_field.data, login_form = login_form)

        user = User.query.filter_by(username = login_form.username.data, password = login_form.password.data).first()

        if not user:
            return render(login_form.view_data_field.data, session_error = "Käyttäjä salasana yhdistelmää ei löytynyt")

        login_user(user)

        return render(login_form.view_data_field.data)

    @staticmethod
    def logout():
        logout_user()
        return redirect(url_for('index'))