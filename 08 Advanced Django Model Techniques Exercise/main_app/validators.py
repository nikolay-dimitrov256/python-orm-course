from django.core.exceptions import ValidationError


class ValidateName:
    def __init__(self, message: str = ''):
        self.message = message

    def __call__(self, value):
        for ch in value:
            if not (ch.isalpha() or ch.isspace()):
                raise ValidationError(message=self.message)

    def deconstruct(self):
        return (
            'main_app.validators.ValidateName',
            (self.message, ),
            {}
        )


def validate_name(value):
    for ch in value:
        if not (ch.isalpha() or ch.isspace()):
            raise ValidationError('Name can only contain letters and spaces')
