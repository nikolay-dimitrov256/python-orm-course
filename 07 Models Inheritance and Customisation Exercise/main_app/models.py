from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models


class MaskedCreditCardField(models.CharField):
    def to_python(self, value):
        if not isinstance(value, str):
            raise ValidationError('The card number must be a string')

        if not value.isdigit():
            raise ValidationError('The card number must contain only digits')

        if len(value) != 16:
            raise ValidationError('The card number must be exactly 16 characters long')

        return value

    def get_prep_value(self, value):
        value = f'****-****-****-{value[-4:]}'

        return value


class StudentIDField(models.PositiveIntegerField):
    def to_python(self, value):
        try:
            value = int(value)
        except ValueError:
            raise ValueError('Invalid input for student ID')

        if value <= 0:
            raise ValidationError('ID cannot be less than or equal to zero')

        return value


class BaseCharacter(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(
        max_length=100,
    )

    description = models.TextField()


class Mage(BaseCharacter):
    elemental_power = models.CharField(
        max_length=100,
    )

    spellbook_type = models.CharField(
        max_length=100,
    )


class Assassin(BaseCharacter):
    weapon_type = models.CharField(
        max_length=100,
    )

    assassination_technique = models.CharField(
        max_length=100,
    )


class DemonHunter(BaseCharacter):
    weapon_type = models.CharField(
        max_length=100,
    )

    demon_slaying_ability = models.CharField(
        max_length=100,
    )


class TimeMage(Mage):
    time_magic_mastery = models.CharField(
        max_length=100,
    )

    temporal_shift_ability = models.CharField(
        max_length=100,
    )


class Necromancer(Mage):
    raise_dead_ability = models.CharField(
        max_length=100,
    )


class ViperAssassin(Assassin):
    venomous_strikes_mastery = models.CharField(
        max_length=100,
    )

    venomous_bite_ability = models.CharField(
        max_length=100,
    )


class ShadowbladeAssassin(Assassin):
    shadowstep_ability = models.CharField(
        max_length=100,
    )


class VengeanceDemonHunter(DemonHunter):
    vengeance_mastery = models.CharField(
        max_length=100,
    )

    retribution_ability = models.CharField(
        max_length=100,
    )


class FelbladeDemonHunter(DemonHunter):
    felblade_ability = models.CharField(
        max_length=100,
    )


class UserProfile(models.Model):
    username = models.CharField(
        max_length=70,
        unique=True,
    )

    email = models.EmailField(
        unique=True,
    )

    bio = models.TextField(
        null=True,
        blank=True,
    )


class Message(models.Model):
    sender = models.ForeignKey(
        to=UserProfile,
        related_name='sent_messages',
        on_delete=models.CASCADE,
    )

    receiver = models.ForeignKey(
        to=UserProfile,
        related_name='received_messages',
        on_delete=models.CASCADE,
    )

    content = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    is_read = models.BooleanField(
        default=False,
    )

    def mark_as_read(self) -> None:
        self.is_read = True

    def reply_to_message(self, reply_content: str) -> 'Message':
        new_message = Message(
            sender=self.receiver,
            receiver=self.sender,
            content=reply_content,
        )

        new_message.save()

        return new_message

    def forward_message(self, receiver: UserProfile) -> 'Message':
        forwarded_message = Message(
            sender=self.receiver,
            receiver=receiver,
            content=self.content,
        )

        forwarded_message.save()

        return forwarded_message


class Student(models.Model):
    name = models.CharField(
        max_length=100,
    )

    student_id = StudentIDField()


class CreditCard(models.Model):
    card_owner = models.CharField(
        max_length=100,
    )

    card_number = MaskedCreditCardField(
        max_length=20,
    )


class Hotel(models.Model):
    name = models.CharField(
        max_length=100,
    )

    address = models.CharField(
        max_length=200,
    )


class Room(models.Model):
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE,
    )

    number = models.CharField(
        max_length=100,
        unique=True,
    )

    capacity = models.PositiveIntegerField()

    total_guests = models.PositiveIntegerField()

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def save(self, *args, **kwargs):
        if self.total_guests > self.capacity:
            raise ValidationError('Total guests are more than the capacity of the room')

        super().save(*args, **kwargs)

        return f'Room {self.number} created successfully'


class BaseReservation(models.Model):
    class Meta:
        abstract = True

    room = models.ForeignKey(
        to=Room,
        on_delete=models.CASCADE,
        # related_name='reservations' # TODO: check for errors
    )

    start_date = models.DateField()
    end_date = models.DateField()

    def reservation_period(self) -> int:
        period = self.end_date - self.start_date

        return period.days

    def calculate_total_cost(self) -> float:
        total_cost = float(self.room.price_per_night) * self.reservation_period()

        return total_cost

    @property
    def reservation_type(self):
        return None

    def save(self, *args, **kwargs):
        if self.start_date <= self.end_date:
            raise ValidationError('Start date cannot be after or in the same end date')

        for reservation in self.room.reservations.all():
            if reservation.start_date <= self.start_date and reservation.start_date >= self.end_date: # TODO: check for equality
                raise ValidationError(f'Room {self.room.number} cannot be reserved')

            if reservation.end_date <= self.start_date and reservation.end_date >= self.end_date: # TODO: check for equality
                raise ValidationError(f'Room {self.room.number} cannot be reserved')

        super().save(*args, **kwargs)

        return f'{self.reservation_type} reservation for room {self.room.number}'


class RegularReservation(BaseReservation):
    @property
    def reservation_type(self):
        return 'Regular'


class SpecialReservation(BaseReservation):
    @property
    def reservation_type(self):
        return 'Special'

    def extend_reservation(self, days: int):
        new_end_date = self.end_date + timedelta(days=days)

        for reservation in self.room.reservations.all():
            if new_end_date <= reservation.start_date:
                raise ValidationError('Error during extending reservation')

        self.end_date = new_end_date

        return f'Extended reservation for room {self.room.number} with {days} days'