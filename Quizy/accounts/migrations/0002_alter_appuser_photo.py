# Generated by Django 4.2.3 on 2023-07-16 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='photo',
            field=models.URLField(blank=True, default='https://lh3.googleusercontent.com/d/1EKocllv5JV28xZSDmSOyioXSY_Uasm1r', null=True),
        ),
    ]
