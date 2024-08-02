import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count
from main_app.models import TennisPlayer


def get_tennis_players(search_name=None, search_country=None) -> str:
    if not search_name and not search_country:
        return ''

    query = ''
    if search_name and search_country:
        query = Q(full_name__icontains=search_name) & Q(country__icontains=search_country)
    elif search_name:
        query = Q(full_name__icontains=search_name)
    elif search_country:
        query = Q(country__icontains=search_country)

    players = TennisPlayer.objects.filter(query).order_by('ranking')
    result = [
        f'Tennis Player: {p.full_name}, country: {p.country}, ranking: {p.ranking}'
        for p in players
    ]

    return '\n'.join(result)


def get_top_tennis_player() -> str:
    top_player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if top_player is None:
        return ''

    return f'Top Tennis Player: {top_player.full_name} with {top_player.matches_won} wins.'


def get_tennis_player_by_matches_count() -> str:
    player = (
        TennisPlayer.objects
        .annotate(matches_played=Count('matches'))
        .order_by('-matches_played', 'ranking')
        .first()
    )

    if player is None or player.matches_played == 0:
        return ''

    return f'Tennis Player: {player.full_name} with {player.matches_played} matches played.'


