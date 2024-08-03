from django.core.validators import MinValueValidator
from django.db import models

from main_app.mixins import NameMixin, LaunchMixin, UpdatedMixin
from main_app.validators import validate_digits
from main_app.choices import SatusChoices
from main_app.managers import AstronautManager


class Astronaut(NameMixin, UpdatedMixin):
    phone_number = models.CharField(
        max_length=15,
        validators=[validate_digits],
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    spacewalks = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )

    objects = AstronautManager()


class Spacecraft(NameMixin, UpdatedMixin, LaunchMixin):
    manufacturer = models.CharField(
        max_length=100,
    )

    capacity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    weight = models.FloatField(
        validators=[MinValueValidator(0.0)]
    )


class Mission(NameMixin, UpdatedMixin, LaunchMixin):
    description = models.TextField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=9,
        choices=SatusChoices.choices,
        default=SatusChoices.PLANNED,
    )

    spacecraft = models.ForeignKey(
        to=Spacecraft,
        on_delete=models.CASCADE,
    )

    astronauts = models.ManyToManyField(
        to=Astronaut,
        related_name='missions',
    )

    commander = models.ForeignKey(
        to=Astronaut,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='missions_commanding',
    )