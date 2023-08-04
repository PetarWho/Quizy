from django.contrib import admin

from Quizy.common.models import HighScore, QuizHistory
from Quizy.quizzes.models import Category, Quiz, Question, Score

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Score)
admin.site.register(HighScore)
admin.site.register(QuizHistory)

