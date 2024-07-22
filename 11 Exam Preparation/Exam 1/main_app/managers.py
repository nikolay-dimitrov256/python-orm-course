from django.db import models
from django.db.models import Count, QuerySet


class DirectorManager(models.Manager):

    def get_directors_by_movies_count(self) -> QuerySet:
        return (self.prefetch_related('movies')
                .annotate(movies_count=Count('movies'))
                .order_by('-movies_count', 'full_name'))
