from django.test import TestCase
from django.contrib.auth import get_user_model
from Quizy.accounts.models import AppUser
from Quizy.quizzes.models import Quiz, Category
from Quizy.common.models import HighScore, QuizHistory

class CommonModelsTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            password='testpassword',
            age=25,
            email='test@example.com'
        )
        self.category = Category.objects.create(name='Test Category', image_url='https://example.com/category-image')
        self.quiz = Quiz.objects.create(
            name='Test Quiz',
            user=self.user,
            category=self.category,
            image_url='https://example.com/quiz-image'
        )

    def test_high_score_model(self):
        high_score = HighScore.objects.create(
            user=self.user,
            quiz=self.quiz,
            score=100
        )
        self.assertEqual(str(high_score), f"High score: {high_score.score} by {self.user.username} in {self.quiz}")

    def test_quiz_history_model(self):
        quiz_history = QuizHistory.objects.create(
            user=self.user,
            quiz=self.quiz,
            score=75
        )
        expected_str = f"{self.user.username} scored {quiz_history.score} on {self.quiz} ({self.quiz.category.name})  at {quiz_history.date.strftime('%B %d, %Y')}"
        self.assertEqual(str(quiz_history), expected_str)
