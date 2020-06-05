from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField, validators
from src.constants import get_required_msg
from src.validators import validate_password

class RegisterForm(FlaskForm):
    username = StringField("Käyttäjätunnus", [validators.InputRequired(message=get_required_msg()), validators.Length(min=4, max=150, message="Tunnus täytyy olla vähintään 4 merkkiä pitkä ja enintään 150 merkkiä pitkä")])
    email = StringField("Sähköposti", [validators.InputRequired(message=get_required_msg()), validators.Email(message="Virheellinen sähköpostiosoite"), validators.Length(max=150, message="Sähköpostiosoite on liian pitkä, maksimipituus 150 merkkiä")])
    first_name = StringField("Etunimi", [validators.InputRequired(message=get_required_msg()), validators.Length(max=150, message="Etunimesi on liian pitkä, maksimipituus 150 merkkiä")])
    last_name = StringField("Sukunimi", [validators.InputRequired(message=get_required_msg()), validators.Length(max=150, message="Sukunimesi on liian pitkä, maksimipituus 150 merkkiä")])
    # 56 max length for password with bcrypt encryption
    password = PasswordField("Salasana", [validators.InputRequired(message=get_required_msg()), validators.Regexp('.*[0-9].*', message='Salasanan täytyy sisältää ainakin yksi numero'), validators.Length(min=8, max=56, message="Salasanan täytyy olla vähintään 8 merkkiä pitkä ja enintään 56 merkkiä pitkä"), validate_password, validators.EqualTo('password_again', 'Salasanat eivät täsmää')])
    password_again = PasswordField("Salasana uudelleen", [validators.InputRequired(message=get_required_msg())])
    view_data_field = HiddenField("_view_data")

    class Meta:
        csrf = False 
