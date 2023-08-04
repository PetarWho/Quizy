from django.db import models
from Quizy.accounts.models import AppUser
from Quizy.quizzes.models import Quiz, Category


class HighScore(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = (("user", "quiz"),)

    def __str__(self):
        return f"High score: {self.score} by {self.user.username} in {self.quiz}"


class QuizHistory(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Quiz Histories"

    def __str__(self):
        return f"Quiz history: {self.user.username}, {self.category} - {self.score} at {self.date}"
