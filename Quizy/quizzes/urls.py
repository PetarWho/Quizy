from django.urls import path
from .views import CategoryCreateView, category_list

urlpatterns = [
    path('c/add/', CategoryCreateView.as_view(), name='add_category'),
    path('c/all/', category_list, name='list_category'),
]