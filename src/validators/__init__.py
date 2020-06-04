from wtforms import validators

def validate_password(form, field):
    special_chars = ["_", "/", "@", "|", "-", "+"]
    if not any(char in field.data for char in special_chars):
        raise validators.ValidationError("Salasanan täytyy sisältää ainakin yksi seuraavista erikoismerkeistä: _, /, @, |, -, +")