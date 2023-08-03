from django.urls import path
from .views import CategoryCreateView, category_list, QuestionCreateView, question_list, QuizCreateView, quiz_list, \
    get_questions, quiz_view

urlpatterns = [
    path('c/add/', CategoryCreateView.as_view(), name='add_category'),
    path('c/all/', category_list, name='list_category'),
    path('q/add/', QuestionCreateView.as_view(), name='add_question'),
    path('q/all/', question_list, name='list_question'),
    path('quiz/add/', QuizCreateView.as_view(), name='add_quiz'),
    path('quiz/all/', quiz_list, name='list_quiz'),
    path('get_questions/', get_questions, name='get_questions'),
    path('quizzing/<int:quiz_id>/', quiz_view, name='start_quiz'),
]
