from flask import request, redirect, url_for, flash
from flask_login import login_user, logout_user
from src.controllers import render
from src.models import User
from src.forms import RegisterForm, LoginForm

class AuthenticationController:
    @staticmethod
    def register_form():
        return render("authentication/register.html", form = RegisterForm())

    @staticmethod
    def register():
        form = RegisterForm(request.form)

        if not form.validate():
            return render("authentication/register.html", form = form)

        user = User(
            form.username.data,
            form.email.data,
            form.first_name.data,
            form.last_name.data,
            form.password.data
        )

        if not user.save():
            flash("Käyttäjätilin luominen epäonnistui", "error")
            return render(form.view_data_field.data, form = form)

        flash("Käyttäjätilin luominen onnistui! Voit kirjautua sisään tunnuksella " + user.username, "success")
        return render("index.html")

    @staticmethod
    def login():
        login_form = LoginForm(request.form)

        if not login_form.validate():
            return render(login_form.view_data_field.data, login_form = login_form)

        user = User.find_by_username_password(login_form.username.data, login_form.password.data)

        if not user:
            flash("Kirjautuminen epäonnistui", "error")
            return render(login_form.view_data_field.data) 

        login_user(user)

        return redirect(url_for("user_private_profile", username = user.username))

    @staticmethod
    def logout():
        logout_user()
        return redirect(url_for('index'))
