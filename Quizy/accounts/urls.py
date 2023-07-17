from django.urls import path
from .views import RegisterUserView, UserLoginView, LogoutView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
