from flask_wtf import FlaskForm
from wtforms import IntegerField, validators
from src.constants import get_required_msg, get_max_integer

class BalanceForm(FlaskForm):
    balance = IntegerField("Määrä", [validators.NumberRange(min=1, max=get_max_integer(), message="Virheellinen määrä minimimäärä 1 € - maksimimäärä " + str(get_max_integer())), validators.InputRequired(message=get_required_msg())])

    class Meta:
        csrf = False
