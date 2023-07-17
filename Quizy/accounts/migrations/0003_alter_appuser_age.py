# Generated by Django 4.2.3 on 2023-07-16 02:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_appuser_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='age',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(120)]),
        ),
    ]
