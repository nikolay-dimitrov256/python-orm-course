import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count, Sum, F, Avg
from main_app.models import Astronaut, Mission, Spacecraft
from main_app.choices import SatusChoices


def get_astronauts(search_string=None) -> str:
    if search_string is None:
        return ''

    query = Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)
    astronauts = Astronaut.objects.filter(query).order_by('name')
    result = [
        f'Astronaut: {a.name}, phone number: {a.phone_number}, status: {"Active" if a.is_active else "Inactive"}'
        for a in astronauts
    ]

    return '\n'.join(result)


def get_top_astronaut() -> str:
    astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()

    if astronaut is None or astronaut.missions_count == 0:
        return 'No data.'

    return f'Top Astronaut: {astronaut.name} with {astronaut.missions_count} missions.'


def get_top_commander() -> str:
    commander = (Astronaut.objects
                 .annotate(missions_count=Count('missions_commanding'))
                 .order_by('-missions_count', 'phone_number')
                 .first()
                 )

    if commander is None or commander.missions_count == 0:
        return 'No data.'

    return f'Top Commander: {commander.name} with {commander.missions_count} commanded missions.'


def get_last_completed_mission() -> str:
    mission = (
        Mission.objects
        .filter(status=SatusChoices.COMPLETED)
        .prefetch_related('astronauts')
        .select_related('spacecraft', 'commander')
        .annotate(spacewalks=Sum('astronauts__spacewalks'))
        .last()
    )

    if mission is None:
        return 'No data.'

    astronauts = ', '.join(a.name for a in mission.astronauts.all().order_by('name'))
    commander = mission.commander.name if mission.commander else 'TBA'

    return (f'The last completed mission is: {mission.name}. Commander: {commander}. Astronauts: {astronauts}. '
            f'Spacecraft: {mission.spacecraft.name}. Total spacewalks: {mission.spacewalks}.')


def get_most_used_spacecraft() -> str:
    spacecraft = (
        Spacecraft.objects
        .annotate(missions_count=Count('mission', distinct=True),
                  astronauts_count=Count('mission__astronauts', distinct=True))
        .order_by('-missions_count', 'name')
        .first()
    )

    if spacecraft is None or spacecraft.missions_count == 0:
        return 'No data.'

    return (f'The most used spacecraft is: {spacecraft.name}, manufactured by {spacecraft.manufacturer}, '
            f'used in {spacecraft.missions_count} missions, astronauts on missions: '
            f'{spacecraft.astronauts_count}.')


def decrease_spacecrafts_weight() -> str:
    affected_spacecrafts = (
        Spacecraft.objects
        .prefetch_related('mission_set')
        .filter(mission__status=SatusChoices.PLANNED, weight__gte=200.0)
        .update(weight=F('weight') - 200.0)
    )

    if affected_spacecrafts == 0:
        return 'No changes in weight.'

    avg_weight = Spacecraft.objects.aggregate(Avg('weight'))["weight__avg"]

    return (f'The weight of {affected_spacecrafts} spacecrafts has been decreased. '
            f'The new average weight of all spacecrafts is {avg_weight:.1f}kg')
