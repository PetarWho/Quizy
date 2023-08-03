# Generated by Django 4.2.3 on 2023-07-27 10:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_appuser_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='age',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(3, message='You have to be at least 3 years old.'), django.core.validators.MaxValueValidator(120, message='Please enter a real age.')]),
        ),
    ]