from django.urls import path

from Quizy.common.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
