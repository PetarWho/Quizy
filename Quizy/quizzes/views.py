from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Category, Question, Quiz
from .forms import CategoryForm, QuestionForm, QuizForm
from ..common.models import QuizHistory, HighScore


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


def quiz_list(request):
    selected_category = request.GET.get('category')
    quizzes = Quiz.objects.all()

    if selected_category:
        quizzes = quizzes.filter(category_id=selected_category)

    paginator = Paginator(quizzes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'quizzes/quiz/quiz_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': int(selected_category) if selected_category else None,
    })


class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'quizzes/quiz/add_quiz.html'
    success_url = reverse_lazy('list_quiz')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass the category choices to the form
        categories = Category.objects.all()
        kwargs['categories'] = categories
        return kwargs

    def form_valid(self, form):
        # Create the quiz instance
        quiz = form.save(commit=False)
        # Associate the user with the quiz
        quiz.user = self.request.user
        # Save the quiz instance
        quiz.save()

        # Add the selected questions to the quiz
        selected_questions = form.cleaned_data['questions']
        quiz.questions.set(selected_questions)

        return super().form_valid(form)


def get_questions(request):
    selected_category_id = request.GET.get('category')
    if selected_category_id:
        questions = Question.objects.filter(category_id=selected_category_id)
        data = [{'id': question.id, 'question_text': question.question_text} for question in questions]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)


def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all()
    user_answers = []  # List to store the user's answers for each question

    if request.method == 'POST':
        for question in questions:
            question_id = question.id
            user_answer = request.POST.get(f'{question_id}_user_answer')

            # Append the user's answer to the list
            user_answers.append(user_answer)

        # If all questions are answered, calculate the score
        if len(user_answers) == questions.count():
            score = 0
            for question, user_answer in zip(questions, user_answers):
                correct_answer = question.correct_answer
                if user_answer == correct_answer:
                    score += 1

            # Check if the user's score is higher than the current high score
            high_score, _ = HighScore.objects.get_or_create(user=request.user, quiz=quiz)
            best = False
            if score > high_score.score:
                high_score.score = score
                high_score.save()
                best = True

            # Display the score
            return render(request, 'quizzes/quiz/quiz_result.html', {'score': score, 'quiz': quiz, 'best': best})

    return render(request, 'quizzes/quiz/quizzing.html', {'questions': questions, 'quiz': quiz})
