import os
import django
from django.db.models import QuerySet

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom
# from populate_db_script import populate_model_with_data
from django.core.paginator import Paginator


# Create queries within functions
def create_pet(name: str, species: str) -> str:
    pet = Pet(name=name, species=species)
    pet.save()

    return f'{pet.name} is a very cute {pet.species}!'


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    artifact = Artifact(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )
    artifact.save()

    return f'The artifact {artifact.name} is {artifact.age} years old!'


def rename_artifact(artifact: Artifact, new_name: str) -> None:
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts() -> None:
    Artifact.objects.all().delete()


def populate_locations() -> None:
    Location.objects.create(
        name='Sofia',
        region='Sofia Region',
        population=1329000,
        description='The capital of Bulgaria and the largest city in the country',
        is_capital=False
    )
    Location.objects.create(
        name='Plovdiv',
        region='Plovdiv Region',
        population=346942,
        description='The second-largest city in Bulgaria with a rich historical heritage',
        is_capital=False
    )
    Location.objects.create(
        name='Varna',
        region='Varna Region',
        population=330486,
        description='A city known for its sea breeze and beautiful beaches on the Black Sea',
        is_capital=False
    )


def show_all_locations() -> str:
    locations = Location.objects.all().order_by('-id')
    result = [f'{l.name} has a population of {l.population}!' for l in locations]

    return '\n'.join(result)


def new_capital() -> None:
    city = Location.objects.first()

    if city is None:
        return

    city.is_capital = True
    city.save()


def get_capitals() -> QuerySet:
    capitals = Location.objects.filter(is_capital=True)

    return capitals.values('name')


def delete_first_location() -> None:
    first_location = Location.objects.first()

    if first_location is None:
        return

    first_location.delete()


def apply_discount() -> None:
    cars = Car.objects.all()

    for car in cars:
        discount_percent = sum(int(d) for d in str(car.year)) / 100
        discount = float(car.price) * discount_percent
        car.price_with_discount = float(car.price) - discount
        car.save()


def get_recent_cars() -> QuerySet:
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car() -> None:
    Car.objects.last().delete()


def show_unfinished_tasks() -> str:
    unfinished_tasks = Task.objects.filter(is_finished=False)
    result = [f'Task - {t.title} needs to be done until {t.due_date}!' for t in unfinished_tasks]

    return '\n'.join(result)


def complete_odd_tasks() -> None:
    tasks = Task.objects.all()

    for task in tasks:
        if task.id % 2 == 1:
            task.is_finished = True

    Task.objects.bulk_update(tasks, ['is_finished'])


def encode_and_replace(text: str, task_title: str) -> None:
    target_tasks = Task.objects.filter(title=task_title)
    text = ''.join(chr(ord(ch) - 3) for ch in text)

    for task in target_tasks:
        task.description = text
        task.save()


def get_deluxe_rooms() -> str:
    deluxe_rooms = HotelRoom.objects.filter(room_type='Deluxe')
    deluxe_rooms = filter(lambda x: x.id % 2 == 0, deluxe_rooms)
    result = [r.info for r in deluxe_rooms]

    return '\n'.join(result)


def increase_room_capacity() -> None:
    rooms = HotelRoom.objects.all().order_by('id')

    for index, room in enumerate(rooms):
        if not room.is_reserved:
            continue

        if index == 0:
            room.capacity += room.id
            continue

        room.capacity += rooms[index - 1].capacity

    HotelRoom.objects.bulk_update(rooms, ['capacity'])


def reserve_first_room() -> None:
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room() -> None:
    last_room = HotelRoom.objects.last()

    if not last_room.is_reserved:
        last_room.delete()


def greet() -> str:
    return 'Hi!'


# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))

# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
# artifact_object = Artifact.objects.get(name='Ancient Sword')
# rename_artifact(artifact_object, 'Ancient Shield')
# print(artifact_object.name)

# populate_locations()
# print(show_all_locations())
# print(new_capital())
# print(get_capitals())

# Paginate queryset with 10 objects per page
# paginator = Paginator(Location.objects.all(), per_page=10)
# [print(x) for x in paginator.page(2)]
