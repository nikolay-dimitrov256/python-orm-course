from django.core.validators import MinLengthValidator
from django.db import models


class PersonalInfoMixin(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)],
    )
    birth_date = models.DateField(
        default='1900-01-01',
    )
    nationality = models.CharField(
        max_length=50,
        default='Unknown',
    )

    class Meta:
        abstract = True


class AwardedMixin(models.Model):
    is_awarded = models.BooleanField(
        default=False,
    )

    class Meta:
        abstract = True


class UpdatedMixin(models.Model):
    last_updated = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True
