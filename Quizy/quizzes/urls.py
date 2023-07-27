from django.urls import path
from .views import CategoryCreateView, category_list, QuestionCreateView, question_list

urlpatterns = [
    path('c/add/', CategoryCreateView.as_view(), name='add_category'),
    path('c/all/', category_list, name='list_category'),
    path('q/add/', QuestionCreateView.as_view(), name='add_question'),
    path('q/all/', question_list, name='list_question'),
]
