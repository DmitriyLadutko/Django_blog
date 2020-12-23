from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import CreateView
from .forms import AuthUserForm, RegistrationUserForm


class LoginUserFormView(LoginView):
    template_name = 'login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return self.success_url


class RegistrationUserView(CreateView):
    model = User
    template_name = 'registration.html'
    form_class = RegistrationUserForm
    success_url = reverse_lazy('login_page')


class ExitSystemView(LogoutView):
    next_page = reverse_lazy('home')
