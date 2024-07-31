import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count, Avg
from main_app.models import Author, Article, Review


def get_authors(search_name=None, search_email=None) -> str:
    if search_name is None and search_email is None:
        return ''

    query = ''
    if search_name and search_email:
        query = Q(full_name__icontains=search_name) & Q(email__icontains=search_email)
    elif search_name:
        query = Q(full_name__icontains=search_name)
    elif search_email:
        query = Q(email__icontains=search_email)

    authors = Author.objects.filter(query).order_by('-full_name')
    result = [f'Author: {a.full_name}, email: {a.email}, status: {"Banned" if a.is_banned else "Not Banned"}'
              for a in authors
              ]

    return '\n'.join(result)


def get_top_publisher() -> str:
    top_author = Author.objects.get_authors_by_article_count().first()

    if top_author is None or top_author.articles_count == 0:
        return ''

    return f'Top Author: {top_author.full_name} with {top_author.articles_count} published articles.'


def get_top_reviewer() -> str:
    top_reviewer = Author.objects.annotate(reviews_count=Count('review')).order_by('-reviews_count', 'email').first()

    if top_reviewer is None or top_reviewer.reviews_count == 0:
        return ''

    return f'Top Reviewer: {top_reviewer.full_name} with {top_reviewer.reviews_count} published reviews.'


def get_latest_article() -> str:
    article = (Article.objects
               .annotate(reviews_count=Count('review'), avg_rating=Avg('review__rating'))
               .prefetch_related('authors')
               .order_by('published_on')
               .last())

    if article is None:
        return ''

    if article.reviews_count == 0:
        article.avg_rating = 0

    authors = ', '.join(a.full_name for a in article.authors.all().order_by('full_name'))
    result = (f'The latest article is: {article.title}. Authors: {authors}. Reviewed: {article.reviews_count} times. '
              f'Average Rating: {article.avg_rating:.2f}.')

    return result


def get_top_rated_article() -> str:
    article = (Article.objects
               .annotate(reviews_count=Count('review'), avg_rating=Avg('review__rating'))
               .order_by('-avg_rating', 'title')
               .first())

    if article is None or article.reviews_count == 0:
        return ''

    result = (f'The top-rated article is: {article.title}, with an average rating '
              f'of {article.avg_rating:.2f}, reviewed {article.reviews_count} times.')

    return result


def ban_author(email=None) -> str:
    if email is None:
        return 'No authors banned.'

    author = Author.objects.filter(email=email).first()

    if author is None:
        return 'No authors banned.'

    author.is_banned = True
    deleted_reviews = author.review_set.all().delete()
    author.save()

    return f'Author: {author.full_name} is banned! {deleted_reviews[0]} reviews deleted.'
