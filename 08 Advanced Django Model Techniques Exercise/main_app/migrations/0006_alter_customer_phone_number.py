# Generated by Django 5.0.4 on 2024-07-13 12:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_customer_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(message="Phone number must start with '+359' followed by 9 digits", regex='^\\+359\\d{9}$')]),
        ),
    ]
