from flask_wtf import FlaskForm
from wtforms import PasswordField, validators
from src.constants import get_required_msg
from src.validators import validate_password

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Vanha salasana", [validators.InputRequired(message=get_required_msg())])
    new_password = PasswordField("Uusi salasana", [validators.InputRequired(message=get_required_msg()), validators.Regexp('.*[0-9].*', message='Salasanan täytyy sisältää ainakin yksi numero'), validators.Length(min=8, max=56, message="Salasanan täytyy olla vähintään 8 merkkiä pitkä ja enintään 56 merkkiä pitkä"), validate_password, validators.EqualTo('new_password_again', 'Salasanat eivät täsmää')])
    new_password_again = PasswordField("Uusi salasana uudelleen", [validators.InputRequired(message=get_required_msg())])

    class Meta:
        csrf = False
