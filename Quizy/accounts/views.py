from django.contrib.auth import logout, login
from django.shortcuts import redirect
from django.views import View
from Quizy.accounts.forms import RegisterUserForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth.mixins import UserPassesTestMixin


def is_anonymous(user):
    return not user.is_authenticated


class RegisterUserView(UserPassesTestMixin, CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')

    def test_func(self):
        return is_anonymous(self.request.user)

    def handle_no_permission(self):
        # Redirect to 'index' or any other URL
        return redirect(reverse('index'))

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UserLoginView(UserPassesTestMixin, LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def test_func(self):
        return is_anonymous(self.request.user)

    def handle_no_permission(self):
        # Redirect to 'index' or any other URL
        return redirect(reverse('index'))

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse('index')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')
