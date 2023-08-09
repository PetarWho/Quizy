from functools import wraps
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView
from .models import Category, Question, Quiz, Score
from .forms import CategoryForm, QuestionForm, QuizForm
from ..common.models import QuizHistory, HighScore
from ..core.view_decorators import is_superuser, is_staff, is_authenticated, is_superuser_or_creator_quiz
from django.contrib import messages
from django.urls import reverse


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

    def dispatch(self, request, *args, **kwargs):
        if not is_staff(request.user):
            messages.error(request, "You are not allowed to add a category.", extra_tags='danger')
            return HttpResponseRedirect(reverse('list_category'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            if form.is_valid():
                messages.success(self.request, "Category created successfully.", extra_tags='success')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"An error occurred: {str(e)}")
            return HttpResponseRedirect(self.get_success_url())


def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if not request.user.has_perm('change_category', category):
        messages.error(request, "You are not allowed to edit this category.", extra_tags='danger')
        return redirect('list_category')

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect('list_category')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'quizzes/category/edit_category.html', {'form': form})


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'quizzes/category/delete_category.html'
    success_url = reverse_lazy('list_category')

    def post(self, request, *args, **kwargs):
        success_message = "Category deleted successfully."
        messages.success(self.request, success_message, extra_tags='success')
        return super().post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('delete_category', self.get_object()):
            messages.error(request, "You are not allowed to delete categories.", extra_tags='danger')
            return redirect('list_category')
        return super().dispatch(request, *args, **kwargs)


@user_passes_test(is_authenticated)
def question_list(request):
    if request.user.is_staff:
        questions = Question.objects.order_by('-pk')
    else:
        questions = Question.objects.filter(user_id=request.user.id)

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


@method_decorator(user_passes_test(is_authenticated), name='dispatch')
class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'quizzes/question/add_question.html'
    success_url = reverse_lazy('list_question')

    def form_valid(self, form):
        flag = True
        try:
            question = form.save(commit=False)
            question.user_id = self.request.user.id

            correct_answer_option = self.request.POST.get('correct_answer')

            if flag:
                if correct_answer_option == 'option1':
                    question.correct_answer = question.option1
                elif correct_answer_option == 'option2':
                    question.correct_answer = question.option2
                elif correct_answer_option == 'option3':
                    question.correct_answer = question.option3
                elif correct_answer_option == 'option4':
                    question.correct_answer = question.option4

                flag = False

            question.save()

            messages.success(self.request, "Question created successfully.", extra_tags='success')
            return redirect('list_question')
        except Exception as e:
            print(str(e))
            messages.error(self.request, f"An error occurred: {str(e)}")
            return HttpResponseRedirect(self.get_success_url())


def edit_question(request, question_id):
    flag = True
    try:
        question = Question.objects.get(pk=question_id)
        if not request.user.is_superuser:
            if question.user_id != request.user.id:
                messages.error(request, "You can only edit questions you've created.", extra_tags='danger')
                return redirect('list_question')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}", extra_tags='danger')
        return redirect('list_question')

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            correct_answer_option = request.POST.get('correct_answer')
            if flag:
                if correct_answer_option == 'option1':
                    question.correct_answer = question.option1
                elif correct_answer_option == 'option2':
                    question.correct_answer = question.option2
                elif correct_answer_option == 'option3':
                    question.correct_answer = question.option3
                elif correct_answer_option == 'option4':
                    question.correct_answer = question.option4

                flag = False

            form.save()
            messages.success(request, "Question updated successfully.", extra_tags='success')
            return redirect('list_question')
    else:
        form = QuestionForm(instance=question)

    return render(request, 'quizzes/question/edit_question.html', {'form': form})


class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'quizzes/question/delete_question.html'
    success_url = reverse_lazy('list_question')

    def dispatch(self, request, *args, **kwargs):
        question = self.get_object()

        if not (request.user.is_superuser or question.user_id == request.user.id):
            messages.error(request, "You are not allowed to delete this question.", extra_tags='danger')
            return redirect('list_question')

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        success_message = "Question deleted successfully."
        messages.success(self.request, success_message, extra_tags='success')
        return super().post(request, *args, **kwargs)


def quiz_list(request):
    selected_category = request.GET.get('category')
    search_query = request.GET.get('search')
    quizzes = Quiz.objects.all().order_by('-pk')

    if selected_category:
        quizzes = quizzes.filter(category_id=selected_category)

    if search_query:
        quizzes = quizzes.filter(Q(name__icontains=search_query) | Q(user__username__icontains=search_query))

    paginator = Paginator(quizzes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'quizzes/quiz/quiz_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': int(selected_category) if selected_category else None,
        'search_query': search_query,
    })


@method_decorator(user_passes_test(is_authenticated), name='dispatch')
class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'quizzes/quiz/edit_quiz.html'
    success_url = reverse_lazy('list_quiz')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        categories = Category.objects.all()
        kwargs['categories'] = categories
        return kwargs

    def form_valid(self, form):
        try:
            quiz = form.save(commit=False)
            quiz.user = self.request.user
            quiz.save()

            selected_questions = form.cleaned_data['questions']
            quiz.questions.set(selected_questions)

            messages.success(self.request, "Quiz created successfully.", extra_tags='success')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"An error occurred: {str(e)}")
            return HttpResponseRedirect(self.get_success_url())


def user_can_edit_quiz(view_func):
    @wraps(view_func)
    def _wrapped_view(request, quiz_id, *args, **kwargs):
        quiz = Quiz.objects.get(pk=quiz_id)

        if request.user.id == quiz.user.id or request.user.is_staff:
            return view_func(request, quiz_id, *args, **kwargs)
        else:
            raise PermissionDenied

    return _wrapped_view


def edit_quiz(request, quiz_id):
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except Quiz.DoesNotExist:
        return redirect('list_quiz')
    categories = Category.objects.all()
    if quiz.user != request.user:
        messages.error(request, "You can only edit quizzes you've created.", extra_tags='danger')
        return redirect('list_quiz')
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz, categories=categories)
        if form.is_valid():
            form.save()
            selected_questions = form.cleaned_data['questions']
            quiz.questions.set(selected_questions)
            messages.success(request, "Quiz updated successfully.", extra_tags='success')
            return redirect('list_quiz')

    else:
        form = QuizForm(instance=quiz, categories=categories)

    return render(request, 'quizzes/quiz/edit_quiz.html', {'form': form})


class IsSuperuserOrCreatorQuizMixin(UserPassesTestMixin):
    def test_func(self):
        quiz_id = self.kwargs['pk']
        return is_superuser_or_creator_quiz(self.request.user, quiz_id)


class QuizDeleteView(IsSuperuserOrCreatorQuizMixin, DeleteView):
    model = Quiz
    template_name = 'quizzes/quiz/delete_quiz.html'
    success_url = reverse_lazy('list_quiz')

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            messages.error(request, "You are not allowed to delete this quiz.", extra_tags='danger')
            return HttpResponseRedirect(reverse('list_quiz'))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        quiz = self.get_object()
        success_message = "Quiz deleted successfully."
        self.object = quiz

        try:
            self.object.delete()
            messages.success(request, success_message, extra_tags='success')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}", extra_tags='danger')

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.success_url


@user_passes_test(is_authenticated)
def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all()
    user_answers = []

    if request.method == 'POST':
        for question in questions:
            question_id = question.id
            user_answer = request.POST.get(f'{question_id}_user_answer')

            user_answers.append(user_answer)

        if len(user_answers) == questions.count():
            score = 0
            for question, user_answer in zip(questions, user_answers):
                correct_answer = question.correct_answer
                if user_answer == correct_answer:
                    score += 1

            QuizHistory.objects.create(quiz=quiz, user=request.user, score=score, date=timezone.now())
            Score.objects.create(score=score, user_id=request.user.id, quiz_id=quiz_id)

            high_score, _ = HighScore.objects.get_or_create(user=request.user, quiz=quiz)
            best = False

            if score > high_score.score:
                high_score.score = score
                high_score.save()
                best = True

            leaderboard_scores = HighScore.objects.filter(quiz_id=quiz.id).order_by('-score')

            return render(request, 'quizzes/quiz/quiz_result.html',
                          {'score': score, 'quiz': quiz, 'best': best, 'leaderboard': leaderboard_scores})

    return render(request, 'quizzes/quiz/quizzing.html', {'questions': questions, 'quiz': quiz})


def get_questions(request):
    selected_category_id = request.GET.get('category')
    if selected_category_id:
        questions = Question.objects.filter(category_id=selected_category_id)
        data = [{'id': question.id, 'question_text': question.question_text} for question in questions]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)


def leaderboard(request, quiz_id):
    try:
        highscore = HighScore.objects.get(user_id=request.user.id, quiz_id=quiz_id)
    except HighScore.DoesNotExist:
        return render(request, 'quizzes/quiz/no-leaderboard.html', {'quiz_id': quiz_id})

    score = highscore.score

    leaderboard_scores = HighScore.objects.filter(quiz_id=quiz_id).order_by('-score')

    return render(request, 'quizzes/quiz/quiz_result.html',
                  {'score': score, 'quiz': highscore.quiz, 'best': False, 'leaderboard': leaderboard_scores})
