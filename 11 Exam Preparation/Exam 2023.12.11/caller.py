import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count
from main_app.models import TennisPlayer, Tournament, Match


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


def get_tournaments_by_surface_type(surface=None) -> str:
    if surface is None:
        return ''

    tournaments = (
        Tournament.objects
        .filter(surface_type__icontains=surface)
        .annotate(matches_count=Count('match'))
        .order_by('-start_date')
    )

    if not tournaments.exists():
        return ''

    result = [
        f'Tournament: {t.name}, start date: {t.start_date}, matches: {t.matches_count}'
        for t in tournaments
    ]

    return '\n'.join(result)


def get_latest_match_info() -> str:
    match = (
        Match.objects
        .prefetch_related('players')
        .select_related('tournament', 'winner')
        .order_by('date_played', 'id')
        .last()
    )

    if match is None:
        return ''

    players = ' vs '.join(p.full_name for p in match.players.all().order_by('full_name'))
    winner = match.winner.full_name if match.winner else 'TBA'

    return (f'Latest match played on: {match.date_played}, tournament: {match.tournament.name}, score: {match.score}, '
            f'players: {players}, winner: {winner}, summary: {match.summary}')


def get_matches_by_tournament(tournament_name=None) -> str:
    if tournament_name is None:
        return 'No matches found.'

    matches = (
        Match.objects
        .select_related('tournament', 'winner')
        .filter(tournament__name__exact=tournament_name)
        .order_by('-date_played')
    )

    if not matches.exists():
        return 'No matches found.'

    result = [
        f'Match played on: {m.date_played}, score: {m.score}, winner: {m.winner.full_name if m.winner else "TBA"}'
        for m in matches
    ]

    return '\n'.join(result)
