from flask import request, redirect, url_for
from src.controllers.base import render
from src.forms.authentication import RegisterForm
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
