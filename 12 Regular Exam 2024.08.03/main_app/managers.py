from django.db.models import Manager, QuerySet, Count


class AstronautManager(Manager):

    def get_astronauts_by_missions_count(self) -> QuerySet:
        return self.annotate(missions_count=Count('missions')).order_by('-missions_count', 'phone_number')
