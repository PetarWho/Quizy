# Generated by Django 4.2.3 on 2023-07-27 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0002_rename_answered_questions_quiz_questions'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='name',
            field=models.CharField(default='test', max_length=30),
            preserve_default=False,
        ),
    ]
