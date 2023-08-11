from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from Quizy.quizzes.models import Category, Question, Quiz, Score
from Quizy.quizzes.forms import CategoryForm, QuestionForm, QuizForm


class QuizzesViewsTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            password='testpassword',
            age=25,
            email='test@example.com'
        )
        self.category = Category.objects.create(
            name='Test Category',
            image_url='https://example.com/category-image'
        )
        self.question = Question.objects.create(
            category=self.category,
            user=self.user,
            question_text='Test Question',
            option1='Option 1',
            option2='Option 2',
            option3='Option 3',
            option4='Option 4',
            correct_answer='option1'
        )
        self.quiz = Quiz.objects.create(
            name='Test Quiz',
            user=self.user,
            category=self.category,
            image_url='https://example.com/quiz-image'
        )
        self.score = Score.objects.create(
            user=self.user,
            quiz=self.quiz,
            score=10
        )

    def test_category_list_view(self):
        response = self.client.get(reverse('list_category'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quizzes/category/category_list.html')

    def test_category_create_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('add_category'))
        self.assertEqual(response.status_code, 302)

    # Test forms
    def test_category_form(self):
        form_data = {'name': 'New Category', 'image_url': 'https://example.com/new-category-image'}
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_question_form(self):
        form_data = {
            'category': self.category,
            'question_text': 'New Question',
            'option1': 'Option 1',
            'option2': 'Option 2',
            'option3': 'Option 3',
            'option4': 'Option 4',
            'correct_answer': 'option1'
        }
        form = QuestionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_quiz_form(self):
        form_data = {
            'category': self.category,
            'image_url': 'https://example.com/new-quiz-image',
            'name': 'New Quiz',
            'questions': [self.question.id]
        }
        form = QuizForm(data=form_data, categories=[self.category])
        self.assertTrue(form.is_valid())
