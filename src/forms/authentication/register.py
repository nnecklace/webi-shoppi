from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

def validate_password(form, field):
    special_chars = ["_", "/", "@", "|", "-", "+"]
    if not any(char in field.data for char in special_chars):
        raise validators.ValidationError("Salasanan täytyy sisältää ainakin yksi seuraavista erikoismerkeistä: _, /, @, |, -, +")

class RegisterForm(FlaskForm):
    required_msg = "Kenttä on pakollinen"
    username = StringField("Käyttäjätunnus", [validators.InputRequired(message=required_msg), validators.Length(min=4, message='Tunnus täytyy olla vähintään 4 merkkiä pitkä')])
    email = StringField("Sähköposti", [validators.InputRequired(message=required_msg), validators.Email(message='Virheellinen sähköpostiosoite')])
    first_name = StringField("Etunimi", [validators.InputRequired(message=required_msg)])
    last_name = StringField("Sukunimi", [validators.InputRequired(message=required_msg)])
    password = PasswordField("Salasana", [validators.InputRequired(message=required_msg), validators.Regexp('0-9', message='Salasanan täytyy sisältää ainakin yksi numero'), validators.Length(min=8, message='Salasanan täytyy olla vähintään 8 merkkiä pitkä'), validate_password, validators.EqualTo('password_again', 'Salasanat eivät täsmää')])
    password_again = PasswordField("Salasana uudelleen", [validators.InputRequired(message=required_msg)])

    class Meta:
        csrf = False 