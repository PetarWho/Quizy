from django.db import models
from Quizy.accounts.models import AppUser
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField()

    def __str__(self):
        return self.name


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255, blank=True, null=True)
    option2 = models.CharField(max_length=255, blank=True, null=True)
    option3 = models.CharField(max_length=255, blank=True, null=True)
    option4 = models.CharField(max_length=255, blank=True, null=True)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text


class Quiz(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    image_url = models.URLField()

    def __str__(self):
        return f"{self.category.name} quiz by {self.user}."


class Score(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()

    def __str__(self):
        return f"Score: {self.score} for {self.user.username} in {self.quiz}"
