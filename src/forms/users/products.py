from flask_wtf import FlaskForm
from wtforms import StringField, validators, FloatField, IntegerField
from src.constants import get_required_msg

class ProductForm(FlaskForm):
    name = StringField("Nimi", [validators.Required(message=get_required_msg())])
    price = FloatField("Hinta", [validators.Required(message=get_required_msg())]) # TODO: Convert to cents
    quantity = IntegerField("Kpl määrä", [validators.Required(message=get_required_msg())])
    
    class Meta:
        csrf = False