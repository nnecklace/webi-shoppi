from flask import request, redirect, url_for
from src.controllers import render
from src.models import User
from src.forms import UserForm, ChangePasswordForm, BalanceForm

class UserController:
    @staticmethod
    def index(username):
        return render("users/main.html", user = User.query.filter_by(username = username).first(), user_form = UserForm(), change_password_form = ChangePasswordForm())

    @staticmethod
    def update(username):
        user_form = UserForm(request.form)
        user = User.query.filter_by(username = username).first()

        if not user_form.validate():
            return render("users/main.html", user = user, user_form = user_form, change_password_form = ChangePasswordForm())

        if not user.update(user_form):
            return render("users/main.html", session_error = "Käyttäjätilin päivittäminen epäonnistui", user = user, user_form = user_form, change_password_form = ChangePasswordForm())

        return render("users/main.html", user = user, user_form = UserForm(), change_password_form = ChangePasswordForm())

    @staticmethod
    def balance_form():
        return render("users/balance_form.html", balance_form = BalanceForm())

    @staticmethod
    def delete(id):
        user = User.query.filter_by(id = id).first()
        if user == None or not user.try_delete():
            return render("users/main.html", session_error = "Käyttäjätilin poistamaminen epäonnistui", user = user, user_form = UserForm(), change_password_form = ChangePasswordForm())

        return redirect(url_for("index"))

    @staticmethod
    def change_password(username):
        change_password_form = ChangePasswordForm(request.form)

        if not change_password_form.validate():
            return render("users/main.html", user = User.query.filter_by(username = username).first(), user_form = UserForm(), change_password_form = change_password_form, password_form_open = True)

        user = User.find_by_username_password(username, change_password_form.old_password.data)

        if not user:
            return render("users/main.html", session_error = "Vahna salasana väärin", user = User.query.filter_by(username = username).first(), user_form = UserForm(), change_password_form = change_password_form, password_form_open = True)

        if not user.update_password(change_password_form.new_password.data):
            return render("users/main.html", session_error = "Salasanan vaihto epäonnistui", user = user, user_form = UserForm(), change_password_form = change_password_form)

        return render("users/main.html", session_success = "Salasanan vaihto onnistui", user = user, user_form = UserForm(), change_password_form = ChangePasswordForm())