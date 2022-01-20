from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UsersCreateFormTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_signup_add_user_in_base(self):
        """При заполнении формы reverse('users:signup')
        создаётся новый пользователь."""
        users_count = User.objects.count()
        form_data = {
            'first_name': 'Oleg',
            'last_name': 'Maslov',
            'username': 'oleg',
            'email': '123@mail.ru',
            'password1': 'oleg1234',
            'password2': 'oleg1234'
        }
        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), users_count + 1)
