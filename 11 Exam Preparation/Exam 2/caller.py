import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count
from main_app.models import Profile, Product, Order


def get_profiles(search_string=None) -> str:
    if search_string is None:
        return ''

    query = Q(full_name__icontains=search_string) | Q(email__icontains=search_string) | Q(phone_number__icontains=search_string)
    profiles = (
        Profile.objects
        .annotate(orders_count=Count('order'))
        .filter(query)
        .order_by('full_name')
    )
    result = [
        f'Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.orders_count}'
        for p in profiles
    ]

    return '\n'.join(result)


def get_loyal_profiles() -> str:
    profiles = Profile.objects.get_regular_customers()
    result = [
        f'Profile: {p.full_name}, orders: {p.orders_count}'
        for p in profiles
    ]

    return '\n'.join(result)


def get_last_sold_products() -> str:
    order = Order.objects.last()
    if not order:
        return ''

    products = order.products.order_by('name')

    if not products.exists():
        return ''

    return f'Last sold products: {", ".join(p.name for p in products)}'


