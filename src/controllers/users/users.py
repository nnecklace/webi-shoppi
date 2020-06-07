from flask import request, redirect, url_for, flash
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
            flash("Käyttäjätilin päivittäminen epäonnistu", "error")
            return render("users/main.html", user = user, user_form = user_form, change_password_form = ChangePasswordForm())

        flash("Tilin tiedot päivitetty", "success")
        return render("users/main.html", user = user, user_form = UserForm(), change_password_form = ChangePasswordForm())

    @staticmethod
    def balance_form():
        return render("users/balance_form.html", balance_form = BalanceForm())

    @staticmethod
    def add_balance(username):
        balance_form = BalanceForm(request.form)

        if not balance_form.validate():
            return render("users/balance_form.html", balance_form = BalanceForm())

        user = User.query.filter_by(username = username).first()

        if not user.set_balance(balance_form.balance.data):
            flash("Saldon päivittäminen epäonnistui", "error")
            return render("users/balance_form.html", balance_form = BalanceForm())

        flash("Saldon pävittäminen onnistui, saldon määrä on " + str(user.balance), "success")
        return render("users/main.html", user = user, user_form = UserForm(), change_password_form = ChangePasswordForm())

    @staticmethod
    def delete(id):
        user = User.query.filter_by(id = id).first()
        if user == None or not user.try_delete():
            flash("Käyttäjätilin poistamaminen epäonnistui", "error")
            return render("users/main.html", user = user, user_form = UserForm(), change_password_form = ChangePasswordForm())

        flash("Käyttäjätili poistettu", "success")
        return redirect(url_for("index"))

    @staticmethod
    def change_password(username):
        change_password_form = ChangePasswordForm(request.form)

        if not change_password_form.validate():
            return render("users/main.html", user = User.query.filter_by(username = username).first(), user_form = UserForm(), change_password_form = change_password_form, password_form_open = True)

        user = User.find_by_username_password(username, change_password_form.old_password.data)

        if not user:
            flash("Väärä vanha salasana", "error")
            return render("users/main.html", user = User.query.filter_by(username = username).first(), user_form = UserForm(), change_password_form = change_password_form, password_form_open = True)

        if not user.update_password(change_password_form.new_password.data):
            flash("Salasanan vaihto epäonnistui", "error")
            return render("users/main.html", user = user, user_form = UserForm(), change_password_form = change_password_form)

        flash("Salasanan vaihto onnistui", "success")
        return render("users/main.html", user = user, user_form = UserForm(), change_password_form = ChangePasswordForm())
