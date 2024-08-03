from django.core.exceptions import ValidationError


def validate_digits(value: str):
    if not value.isdigit():
        raise ValidationError('Phone number must contain only digits')
