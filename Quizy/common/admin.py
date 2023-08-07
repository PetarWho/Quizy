from django.contrib import admin

from Quizy.common.models import HighScore, QuizHistory


class HighScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score')
    list_filter = ('quiz__category', 'user')
    search_fields = ('user__username', 'quiz__name')


admin.site.register(HighScore, HighScoreAdmin)


class QuizHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'quiz', 'date')
    list_filter = ('quiz__category', 'user')
    search_fields = ('user__username', 'quiz__name')
    date_hierarchy = 'date'


admin.site.register(QuizHistory, QuizHistoryAdmin)
