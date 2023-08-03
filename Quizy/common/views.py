from django.views.generic import TemplateView
from .models import Category
import random


class IndexView(TemplateView):
    template_name = 'common/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all().order_by('pk').values()
        context['categories'] = categories
        return context
