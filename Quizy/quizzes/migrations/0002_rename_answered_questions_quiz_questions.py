# Generated by Django 4.2.3 on 2023-07-27 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='answered_questions',
            new_name='questions',
        ),
    ]