from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from src.constants import get_required_msg

class LoginForm(FlaskForm):
    username = StringField("Käyttäjätunnus", [validators.InputRequired(message=get_required_msg())])
    password = PasswordField("Salasana", [validators.InputRequired(message=get_required_msg())])

    class Meta:
        csrf = False