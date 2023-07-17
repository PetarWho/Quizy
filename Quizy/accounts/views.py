from django.contrib.auth import logout, login
from django.shortcuts import redirect
from django.views import View
from Quizy.accounts.forms import RegisterUserForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView


class RegisterUserView(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect(reverse('index'))


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')
