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
            title='Test group',
            slug='test-slug',
            description='Test description',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Test post',
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTests.user)

    # Checking public pages
    def test_posts_all_urls_guest_client(self):
        """The pages /, group/test-slug/, profile/auth/,
        posts/1/ are available to any user."""
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

    # Checking the availability of pages for an authorized user
    def test_create_post_url_autorized(self):
        """The create/ page is available to the authorized user."""
        response = self.authorized_client.get('/create/')
        self.assertEquals(response.status_code, HTTPStatus.OK)

    def test_edit_post_url_autor(self):
        """The posts/1/edit/ page is available to the author."""
        response = self.authorized_client.get(
            f'/posts/{PostURLTests.post.id}/edit/')
        self.assertEquals(response.status_code, HTTPStatus.OK)

    # Checking redirects for unauthorized users
    def test_create_post_url_anonymous_on_admin_login(self):
        """The create/ page will redirect the anonymous
        user to the login page."""
        response = self.client.get('/create/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_edit_post_url_anonymous_on_admin_login(self):
        """The posts/1/edit/ page will redirect the anonymous
        user to the login page."""
        response = self.client.get(
            f'/posts/{PostURLTests.post.id}/edit/', follow=True)
        self.assertRedirects(
            response, f'/auth/login/?next=/posts/{PostURLTests.post.id}/edit/')

    def test_add_comment_url_anonymous_on_admin_login(self):
        """The posts/1/comment page will redirect the anonymous
        user to the login page."""
        response = self.client.get(
            f'/posts/{PostURLTests.post.id}/comment/', follow=True)
        self.assertRedirects(
            response,
            f'/auth/login/?next=/posts/{PostURLTests.post.id}/comment/')

    # Checking the called patterns for each address
    def test_urls_uses_correct_template(self):
        """The URL uses the appropriate template."""
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
        """The unexisting_page/ page will return a 404 error"""
        response = self.client.get('/unexisting_page/')
        self.assertEquals(response.status_code, HTTPStatus.NOT_FOUND)
