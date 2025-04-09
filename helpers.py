import string
from datetime import datetime


# Checks if a password meets validity criteria: at least 8 characters, contains a digit, and a special character
def is_valid_password(password):
    return (
        len(password) >= 8
        and any(c.isdigit() for c in password)
        and any(c in string.punctuation for c in password)
    )


# Validates whether a given string is a valid date in the format DD/MM/YYYY
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False


# Checks if a given value can be converted to a valid number (integer or float)
def is_valid_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
