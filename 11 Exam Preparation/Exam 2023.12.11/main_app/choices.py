from django.db.models import TextChoices


class SurfaceChoices(TextChoices):
    NOT_SELECTED = 'Not Selected', 'Not Selected'
    CLAY = 'Clay', 'Clay'
    GRASS = 'Grass', 'Grass'
    HARD_COURT = 'Hard Court', 'Hard Court'
