from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core import validators
from Quizy.core.validators import validate_only_letters


class AppUser(AbstractUser):
    MIN_LEN_NAME = 2
    MAX_LEN_NAME = 30
    MIN_AGE_VALUE = 3
    MAX_AGE_VALUE = 120

    first_name = models.CharField(max_length=MAX_LEN_NAME,
                                  validators=(
                                    validators.MinLengthValidator(MIN_LEN_NAME),
                                    validate_only_letters
                                  ))
    last_name = models.CharField(max_length=MAX_LEN_NAME,
                                 validators=(
                                     validators.MinLengthValidator(MIN_LEN_NAME),
                                     validate_only_letters
                                 ))
    age = models.PositiveIntegerField(validators=(
        validators.MinValueValidator(MIN_AGE_VALUE, message="You have to be at least 3 years old."),
        validators.MaxValueValidator(MAX_AGE_VALUE, message="Please enter a real age."),
    ))
    email = models.EmailField(unique=True)
    photo = models.URLField(null=True, blank=True, default="https://lh3.googleusercontent.com/d/1EKocllv5JV28xZSDmSOyioXSY_Uasm1r")


