from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField, validators
from src.constants import get_required_msg
from src.validators import validate_password

class RegisterForm(FlaskForm):
    username = StringField("Käyttäjätunnus", [validators.InputRequired(message=get_required_msg()), validators.Length(min=4, message='Tunnus täytyy olla vähintään 4 merkkiä pitkä')])
    email = StringField("Sähköposti", [validators.InputRequired(message=get_required_msg()), validators.Email(message='Virheellinen sähköpostiosoite')])
    first_name = StringField("Etunimi", [validators.InputRequired(message=get_required_msg())])
    last_name = StringField("Sukunimi", [validators.InputRequired(message=get_required_msg())])
    password = PasswordField("Salasana", [validators.InputRequired(message=get_required_msg()), validators.Regexp('.*[0-9].*', message='Salasanan täytyy sisältää ainakin yksi numero'), validators.Length(min=8, message='Salasanan täytyy olla vähintään 8 merkkiä pitkä'), validate_password, validators.EqualTo('password_again', 'Salasanat eivät täsmää')])
    password_again = PasswordField("Salasana uudelleen", [validators.InputRequired(message=get_required_msg())])
    view_data_field = HiddenField("_view_data")

    class Meta:
        csrf = False 
