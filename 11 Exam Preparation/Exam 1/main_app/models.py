from django.core.validators import MinValueValidator, MinLengthValidator, MaxLengthValidator, MaxValueValidator
from django.db import models

from main_app.mixins import PersonalInfoMixin, AwardedMixin, UpdatedMixin
from main_app.choices import GenreChoices


class Director(PersonalInfoMixin):
    years_of_experience = models.SmallIntegerField(
        validators=[MinValueValidator(0)],
        default=0,
    )


class Actor(PersonalInfoMixin, AwardedMixin, UpdatedMixin):
    pass


class Movie(AwardedMixin, UpdatedMixin):
    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)],
    )

    release_date = models.DateField()

    storyline = models.TextField(
        null=True,
        blank=True,
    )

    genre = models.CharField(
        max_length=6,
        choices=GenreChoices.choices,
        default=GenreChoices.OTHER,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        default=0.0,
    )

    is_classic = models.BooleanField(
        default=False,
    )

    director = models.ForeignKey(
        to=Director,
        on_delete=models.CASCADE,
        related_name='movies',
    )

    starring_actor = models.ForeignKey(
        to=Actor,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='starring_movies',
    )

    actors = models.ManyToManyField(
        to=Actor,
        related_name='movies'
    )
