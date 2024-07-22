import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


# Import your models here
from django.db.models import Q, Count, Avg, F
from main_app.models import Director, Actor, Movie


# Create queries within functions


def get_directors(search_name=None, search_nationality=None) -> str:
    if search_name is None and search_nationality is None:
        return ''

    name_query = Q(full_name__icontains=search_name)
    nationality_query = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query = name_query & nationality_query
    elif search_name is None:
        query = nationality_query
    else:
        query = name_query

    directors = Director.objects.filter(query).order_by('full_name')

    result = [
        f'Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}'
        for d in directors
    ]

    return '\n'.join(result)


def get_top_director() -> str:
    top_director = Director.objects.get_directors_by_movies_count().first()

    if top_director is None:
        return ''

    return f'Top Director: {top_director.full_name}, movies: {top_director.movies_count}.'


def get_top_actor() -> str:
    top_actor = (
        Actor.objects
        .prefetch_related('starring_movies')
        .annotate(total_movies=Count('starring_movies'), average_rating=Avg('starring_movies__rating'))
        .order_by('-total_movies', 'full_name')
        .first()
    )

    if top_actor is None or top_actor.total_movies == 0:
        return ''

    movies = ', '.join(m.title for m in top_actor.starring_movies.all())

    return (f'Top Actor: {top_actor.full_name}, starring in movies: {movies}, '
            f'movies average rating: {top_actor.average_rating:.1f}')


def get_actors_by_movies_count() -> str:
    actors = (
        Actor.objects
        .prefetch_related('movies')
        .annotate(movies_count=Count('movies'))
        .order_by('-movies_count', 'full_name')[:3]
    )

    if not actors.exists() or actors[0].movies_count == 0:
        return ''

    result = [f'{a.full_name}, participated in {a.movies_count} movies' for a in actors]

    return '\n'.join(result)


def get_top_rated_awarded_movie() -> str:
    top_movie = (
        Movie.objects
        .filter(is_awarded=True)
        .prefetch_related('actors')
        .select_related('starring_actor')
        .order_by('-rating', 'title')
        .first()
    )

    if top_movie is None:
        return ''

    starring = top_movie.starring_actor.full_name if top_movie.starring_actor else 'N/A'
    cast = ', '.join(a.full_name for a in top_movie.actors.all().order_by('full_name'))

    return (f'Top rated awarded movie: {top_movie.title}, rating: {top_movie.rating:.1f}. '
            f'Starring actor: {starring}. Cast: {cast}.')


def increase_rating() -> str:
    updated_movies = (
        Movie.objects
        .filter(is_classic=True, rating__lt=10.0)
        .update(rating=F('rating') + 0.1)
    )

    if updated_movies == 0:
        return 'No ratings increased.'

    return f'Rating increased for {updated_movies} movies.'
