from django.urls import path

from .views import LoginUserFormView, RegistrationUserView, ExitSystemView

urlpatterns = [
    path('login/', LoginUserFormView.as_view(), name='login_page'),
    path('registration/', RegistrationUserView.as_view(), name='registration_page'),
    path('exit/', ExitSystemView.as_view(), name='exit_page'),
]
