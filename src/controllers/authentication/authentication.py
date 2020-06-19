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

        if User.query.filter_by(username = form.username.data).first():
            flash("Käyttäjätunnus on jo rekisteröity", "error")
            return redirect(request.referrer)

        user = User(
            form.username.data,
            form.email.data,
            form.first_name.data,
            form.last_name.data,
            form.password.data
        )

        if not user.save("user create:"):
            flash("Käyttäjätilin luominen epäonnistui", "error")
            return redirect(request.referrer)

        flash("Käyttäjätilin luominen onnistui! Voit kirjautua sisään tunnuksella " + user.username, "success")
        return render("index.html")

    @staticmethod
    def login():
        login_form = LoginForm(request.form)

        if not login_form.validate():
            flash("Kirjautuminen epäonnistui", "error")
            return redirect(request.referrer)

        user = User.find_by_username_password(login_form.username.data, login_form.password.data)

        if not user:
            flash("Kirjautuminen epäonnistui", "error")
            return redirect(request.referrer)

        login_user(user)

        return redirect(url_for("user_private_profile", username = user.username))

    @staticmethod
    def logout():
        logout_user()
        return redirect(url_for('index'))
