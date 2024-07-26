import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count, F, Case, When, Value
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


def get_top_products() -> str:
    products = (
        Product.objects
        .annotate(sales=Count('order'))
        .filter(sales__gt=0)
        .order_by('-sales', 'name')[:5]
    )

    if not products.exists():
        return ''

    result = ['Top products:'] + [f'{p.name}, sold {p.sales} times' for p in products]

    return '\n'.join(result)


def apply_discounts() -> str:
    updated_orders = (
        Order.objects
        .annotate(products_count=Count('products'))
        .filter(products_count__gt=2, is_completed=False)
        .update(total_price=F('total_price') * 0.9)
    )

    return f'Discount applied to {updated_orders} orders.'


def complete_order() -> str:
    order = Order.objects.filter(is_completed=False).first()

    if not order:
        return ''

    order.products.update(
        in_stock=F('in_stock') - 1,
        is_available=Case(
            When(in_stock=1, then=Value(False)),
            default=F('is_available')
        )
    )

    order.is_completed = True
    order.save()

    return 'Order has been completed!'
