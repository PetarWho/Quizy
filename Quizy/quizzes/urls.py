from django.urls import path
from .views import *

urlpatterns = [
    # Category
    path('c/add/', CategoryCreateView.as_view(), name='add_category'),
    path('c/edit/<int:category_id>', edit_category, name='edit_category'),
    path('c/<int:pk>/delete/', CategoryDeleteView.as_view(), name='delete_category'),
    path('c/all/', category_list, name='list_category'),

    # Question
    path('q/add/', QuestionCreateView.as_view(), name='add_question'),
    path('q/all/', question_list, name='list_question'),
    path('q/edit/<int:question_id>', edit_question, name='edit_question'),
    path('q/<int:pk>/delete/', QuestionDeleteView.as_view(), name='delete_question'),
    # Quiz
    path('quiz/add/', QuizCreateView.as_view(), name='add_quiz'),
    path('quiz/all/', quiz_list, name='list_quiz'),
    path('quizzing/<int:quiz_id>/', quiz_view, name='start_quiz'),
]
