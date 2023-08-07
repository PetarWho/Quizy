from django.contrib import admin
from Quizy.quizzes.models import Category, Quiz, Question, Score


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_url')
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'category', 'user')
    list_filter = ('category',)
    search_fields = ('question_text',)


admin.site.register(Question, QuestionAdmin)


class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'user')
    list_filter = ('category', 'user')
    search_fields = ('name',)


admin.site.register(Quiz, QuizAdmin)


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score')
    list_filter = ('quiz', 'user')
    search_fields = ('user__username',)


admin.site.register(Score, ScoreAdmin)
