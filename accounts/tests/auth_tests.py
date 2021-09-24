from unittest.mock import Mock, patch

from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from faker import Faker

from accounts.forms import UserRegistrationForm


User = get_user_model()
fake = Faker()


class UserRegistrationFormTest(TestCase):

    @patch('accounts.models.User.get_user_by_email')
    def test_success_clean_email(self, mock_get_user_by_email):
        rand_email: str = fake.ascii_company_email()

        form: UserRegistrationForm = UserRegistrationForm()
        setattr(form, 'cleaned_data', {'email': rand_email})

        mock_get_user_by_email.return_value = None

        self.assertEqual(form.clean_email(), rand_email)

    @patch('accounts.models.User.get_user_by_email')
    def test_fail_clean_email_via_duplication(self, mock_get_user_by_email):
        rand_email: str = fake.ascii_company_email()
        existing_user: Mock = Mock(spec=User)
        existing_user.email = rand_email

        form: UserRegistrationForm = UserRegistrationForm()
        setattr(form, 'cleaned_data', {'email': rand_email})

        mock_get_user_by_email.return_value = existing_user

        with self.assertRaises(ValidationError):
            form.clean_email()

    @patch('accounts.models.User.get_user_by_nickname')
    def test_success_clean_nickname(self, mock_get_user_by_nickname):
        rand_nickname: str = fake.user_name()

        form: UserRegistrationForm = UserRegistrationForm()
        setattr(form, 'cleaned_data', {'nickname': rand_nickname})

        mock_get_user_by_nickname.return_value = None

        self.assertEqual(form.clean_nickname(), rand_nickname)

    @patch('accounts.models.User.get_user_by_nickname')
    def test_fail_clean_nickname_via_duplication(self, mock_get_user_by_nickname):
        rand_nickname: str = fake.user_name()
        existing_user: Mock = Mock(spec=User)
        existing_user.nickname = rand_nickname

        form: UserRegistrationForm = UserRegistrationForm()
        setattr(form, 'cleaned_data', {'nickname': rand_nickname})

        mock_get_user_by_nickname.return_value = existing_user

        with self.assertRaises(ValidationError):
            form.clean_nickname()


class UserLoginTest(TestCase):

    def test_success_user_login(self):
        rand_email = fake.ascii_company_email()
        rand_password = fake.password(length=18)
        c = Client()
        c.login(email=rand_email, password=rand_password)
