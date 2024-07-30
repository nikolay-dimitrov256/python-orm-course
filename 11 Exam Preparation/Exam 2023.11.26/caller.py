import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count
from main_app.models import Author, Article, Review
from datetime import datetime
import random


# Create queries within functions
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
