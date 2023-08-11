from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class AccountsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()

        self.user = self.User.objects.create_user(
            username='testuser',
            password='testpassword',
            age=25,
            email='test@example.com'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_user_profile_view(self):
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_edit_profile_view(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/edit_profile.html')

    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword',
            'age': 30,
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_login_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_user_profile_view_logged_in(self):
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_edit_profile_view_get(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/edit_profile.html')


class AccountsModelTests(TestCase):
    def test_user_str_representation(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            age=25,
            email='test@example.com'
        )
        self.assertEqual(str(user), 'testuser')
