from flask import render_template, request, redirect, url_for
from src.forms.authentication import RegisterForm
from src.db import db

class AuthenticationController:
    @staticmethod
    def register_form():
        return render_template("authentication/register.html", form = RegisterForm())

    @staticmethod
    def register():
        form = RegisterForm(request.form)

        if not form.validate():
            for error in form.username.errors:
                print(error)
            return render_template("authentication/register.html", form = form)

        return render_template("index.html")