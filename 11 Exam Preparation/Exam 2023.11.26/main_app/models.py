from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.managers import AuthorManager
from main_app.mixins import ContentMixin, PublishedMixin
from main_app.choices import CategoryChoices


class Author(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)]
    )

    email = models.EmailField(
        unique=True,
    )

    is_banned = models.BooleanField(
        default=False,
    )

    birth_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2005),
        ]
    )

    website = models.URLField(
        null=True,
        blank=True,
    )

    objects = AuthorManager()


class Article(ContentMixin, PublishedMixin):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(5)],
    )

    category = models.CharField(
        max_length=10,
        choices=CategoryChoices.choices,
        default=CategoryChoices.TECHNOLOGY,
    )

    authors = models.ManyToManyField(
        to=Author,
    )


class Review(ContentMixin, PublishedMixin):
    rating = models.FloatField(
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(5.0),
        ]
    )

    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
    )

    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE,
    )
