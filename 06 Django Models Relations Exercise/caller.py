import os
from datetime import timedelta, date

import django
from django.db.models import QuerySet

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Artist, Song, Product, Review, DrivingLicense, Driver, Owner, Registration, \
    Car


# Create queries within functions
def show_all_authors_with_their_books() -> str:
    authors = Author.objects.all().order_by('id')
    result = []

    #result = [f'{a.name} has written - {", ".join(str(b) for b in a.book_set.all())}!' for a in authors if a.book_set.all()]

    for author in authors:
        books = ', '.join(str(b) for b in author.book_set.all())
        if books:
            result.append(f'{author.name} has written - {books}!')

    return '\n'.join(result)


def delete_all_authors_without_books() -> None:
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)


def get_songs_by_artist(artist_name: str) -> QuerySet:
    artist = Artist.objects.get(name=artist_name)

    return artist.songs.all().order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str) -> None:
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str) -> float:
    product = Product.objects.get(name=product_name)
    reviews = product.reviews.all()
    avg_rating = sum(r.rating for r in reviews) / len(reviews)

    return avg_rating


def get_reviews_with_high_ratings(threshold: int) -> QuerySet:
    reviews = Review.objects.filter(rating__gte=threshold)

    return reviews


def get_products_with_no_reviews() -> QuerySet:
    no_review_products = Product.objects.filter(reviews__isnull=True).order_by('-name')

    return no_review_products


def delete_products_without_reviews() -> None:
    Product.objects.filter(reviews__isnull=True).delete()


def calculate_licenses_expiration_dates() -> str:
    all_licenses = DrivingLicense.objects.all().order_by('-license_number')
    result = []

    for l in all_licenses:
        expiration_date = l.issue_date + timedelta(days=365)
        result.append(f'License with number: {l.license_number} expires on {expiration_date}!')

    return '\n'.join(result)


def get_drivers_with_expired_licenses(due_date: date) -> None:
    cutoff_date = due_date - timedelta(days=365)
    drivers_with_expired_license = Driver.objects.filter(license__issue_date__gt=cutoff_date)

    return drivers_with_expired_license


def register_car_by_owner(owner: Owner) -> str:
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()

    # if not registration or not car:
    #     return

    registration.registration_date = date.today()
    registration.car = car
    registration.save()
    owner.cars.add(car)
    car.save()

    return f'Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}.'


# for a in Author.objects.all():
#     print(', '.join(b.title for b in a.book_set.all()))

# for b in Book.objects.all():
#     print(f'"{b.title}" by {b.author.name}')

Car.objects.bulk_update(Car(model='Civic'), )