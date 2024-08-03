from django.db.models import TextChoices


class SatusChoices(TextChoices):
    PLANNED = 'Planned', 'Planned'
    ONGOING = 'Ongoing', 'Ongoing'
    COMPLETED = 'Completed', 'Completed'
