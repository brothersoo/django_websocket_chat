from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from accounts.forms import UserLoginForm, UserRegistrationForm


class UserRegistrationView(CreateView):
    model = get_user_model()
    form_class = UserRegistrationForm
    success_url = '/accounts/login/'


class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'accounts/login_form.html'
    redirect_field_name = '/chats/'

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)
