from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

# Create your models here.
from main_app.validators import validate_name


class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[validate_name]
    )

    age = models.PositiveIntegerField(
        validators=[
            MinValueValidator(18, message='Age must be greater than or equal to 18')
        ]
    )

    email = models.EmailField(
        error_messages={'invalid': 'Enter a valid email address'}
    )

    phone_number = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(regex=r'^\+359\d{9}$', message="Phone number must start with '+359' followed by 9 digits")
        ]
    )

    website_url = models.URLField(
        error_messages={'invalid': 'Enter a valid URL'}
    )
