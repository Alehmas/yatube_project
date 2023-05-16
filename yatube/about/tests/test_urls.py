from http import HTTPStatus

from django.test import Client, TestCase


class AboutURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_urls(self):
        """Checking availability of /about/author/, /about/tech/."""
        about_url_names = {
            '/about/author/': HTTPStatus.OK,
            '/about/tech/': HTTPStatus.OK,
        }
        for url, status_code in about_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEquals(response.status_code, status_code)

    def test_about_url_uses_correct_template(self):
        """Checking templates for /about/author/, /about/tech/."""
        about_url_names = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }
        for url, template in about_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
