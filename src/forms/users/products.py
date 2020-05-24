from flask_wtf import FlaskForm
from wtforms import StringField, validators, FloatField, IntegerField
from src.constants import get_required_msg

class ProductForm(FlaskForm):
    name = StringField("Nimi", [validators.Required(message=get_required_msg()), validators.Length(max=150, message="Tuotteen nimi on liian pitkä. Maksimipituus 150.")])
    price = FloatField("Hinta (€)", [validators.Required(message=get_required_msg()), validators.NumberRange(min=1, max=1073741824, message="Minimihinta on 1 € ja maksimihinta on 1073741824")])
    quantity = IntegerField("Kpl määrä", [validators.NumberRange(min=1, max=1073741824, message="Kpl määrä täytyy olla vähintään yksi (1) ja saa maksimissaan olla 1073741824")])
    
    class Meta:
        csrf = False