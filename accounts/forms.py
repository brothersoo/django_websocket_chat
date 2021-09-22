from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import EmailField
from django.utils.translation import ugettext_lazy as _


User = get_user_model()


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'nickname')

    def clean_email(self):
        self.error_messages['existing_email'] = _('Already existing email')
        email = self.cleaned_data.get("email")
        if User.get_user_by_email(email):
            raise ValidationError(
                self.error_messages['existing_email'],
                code='existing_email',
            )
        return email

    def clean_nickname(self):
        self.error_messages['existing_nickname'] = _('Already existing nickname')
        nickname = self.cleaned_data.get("nickname")
        if User.get_user_by_nickname():
            raise ValidationError(
                self.error_messages['existing_nickname'],
                code='existing_nickname',
            )
        return nickname


class UserLoginForm(AuthenticationForm):
    username = EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
