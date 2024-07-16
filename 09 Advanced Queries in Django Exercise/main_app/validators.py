from django.core.exceptions import ValidationError


class RangeValidator:
    def __init__(self, min_value, max_value, message=''):
        self.min_value = min_value
        self.max_value = max_value
        self.message = message

    def __call__(self, value):
        if not self.min_value <= value <= self.max_value:
            raise ValidationError(message=self.message)

    def deconstruct(self):
        return (
            'main_app.validators.RangeValidator',
            (self.min_value, self.max_value),
            {'message': self.message}
        )
