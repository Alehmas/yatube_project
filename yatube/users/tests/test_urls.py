from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class UsersURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(UsersURLTests.user)

    # Проверяем общедоступные страницы
    def test_users_url_guest_client(self):
        """Страница auth/signup/, auth/login/, auth/password_reset/,
        auth/password_reset/done/, auth/auth/reset/NQ/set-password/,
        auth/reset/done/ доступна любому пользователю."""
        users_url_names = {
            '/auth/signup/': 200,
            '/auth/login/': 200,
            '/auth/password_reset/': 200,
            '/auth/password_reset/done/': 200,
            '/auth/reset/NQ/set-password/': 200,
            '/auth/reset/done/': 200,
        }
        for url, status_code in users_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEquals(response.status_code, status_code)

    # Проверяем доступность страниц для авторизованного пользователя
    def test_users_url_authorized_url(self):
        """Страница auth/password_change/, auth/password_change/done/,
        auth/logout/ доступна авторизованному пользователю."""
        users_url_names = {
            '/auth/password_change/': 200,
            '/auth/password_change/done/': 200,
            '/auth/logout/': 200,
        }
        for url, status_code in users_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEquals(response.status_code, status_code)

    # Проверяем редиректы для неавторизованного пользователя
    def test_users_password_change_url_anonymous_on_admin_login(self):
        """Страница /auth/password_change/ перенаправит анонимного
        пользователя на страницу логина."""
        response = self.guest_client.get(
            '/auth/password_change/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/auth/password_change/')
