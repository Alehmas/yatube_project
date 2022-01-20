from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from posts.models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTests.user)

    # Проверяем общедоступные страницы
    def test_posts_all_urls_guest_client(self):
        """Страницы /, group/test-slug/, profile/auth/,
        posts/1/ доступны любому пользователю."""
        posts_url_names = {
            '/': HTTPStatus.OK,
            f'/group/{PostURLTests.group.slug}/': HTTPStatus.OK,
            f'/profile/{PostURLTests.post.author}/': HTTPStatus.OK,
            f'/posts/{PostURLTests.post.id}/': HTTPStatus.OK,
        }
        for url, status_code in posts_url_names.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEquals(response.status_code, status_code)

    # Проверяем доступность страниц для авторизованного пользователя
    def test_create_post_url_autorized(self):
        """Страница create/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEquals(response.status_code, HTTPStatus.OK)

    def test_edit_post_url_autor(self):
        """Страница posts/1/edit/ доступна автору."""
        response = self.authorized_client.get(
            f'/posts/{PostURLTests.post.id}/edit/')
        self.assertEquals(response.status_code, HTTPStatus.OK)

    # Проверяем редиректы для неавторизованного пользователя
    def test_create_post_url_anonymous_on_admin_login(self):
        """Страница create/ перенаправит анонимного
        пользователя на страницу логина."""
        response = self.client.get('/create/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_edit_post_url_anonymous_on_admin_login(self):
        """Страница posts/1/edit/ перенаправит анонимного
        пользователя на страницу логина."""
        response = self.client.get(
            f'/posts/{PostURLTests.post.id}/edit/', follow=True)
        self.assertRedirects(
            response, f'/auth/login/?next=/posts/{PostURLTests.post.id}/edit/')

    # Проверка вызываемых шаблонов для каждого адреса
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{PostURLTests.group.slug}/': 'posts/group_list.html',
            f'/profile/{PostURLTests.post.author}/': 'posts/profile.html',
            f'/posts/{PostURLTests.post.id}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{PostURLTests.post.id}/edit/': 'posts/create_post.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_unexisting_page(self):
        """Страница unexisting_page/ вернет ошибку 404"""
        response = self.client.get('/unexisting_page/')
        self.assertEquals(response.status_code, HTTPStatus.NOT_FOUND)
