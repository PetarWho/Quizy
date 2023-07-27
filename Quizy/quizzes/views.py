from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Category, Question
from .forms import CategoryForm, QuestionForm


def category_list(request):
    categories = Category.objects.all()

    paginator = Paginator(categories, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'quizzes/category/category_list.html', {'page_obj': page_obj})


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'quizzes/category/add_category.html'
    success_url = reverse_lazy('list_category')


def question_list(request):
    questions = Question.objects.all()

    selected_category = request.GET.get('category')
    if selected_category:
        questions = questions.filter(category_id=selected_category)

    paginator = Paginator(questions, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'quizzes/question/question_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': int(selected_category) if selected_category else None,
    })


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'quizzes/question/add_question.html'
    success_url = reverse_lazy('list_question')
