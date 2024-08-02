from django.db.models import Manager, QuerySet, Count


class TennisPlayerManager(Manager):

    def get_tennis_players_by_wins_count(self) -> QuerySet:
        return self.annotate(matches_won=Count('won_matches')).order_by('-matches_won', 'full_name')
