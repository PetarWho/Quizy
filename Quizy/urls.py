from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("Quizy.common.urls")),
    path('account/', include("Quizy.accounts.urls")),
    path('quizzes/', include("Quizy.quizzes.urls")),
]
