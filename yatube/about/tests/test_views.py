from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class AboutViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_page_accessible_by_name(self):
        """URLs, генерируемыe при помощи имен 'about:author',
        'about:tech' доступены."""
        about_name_urls = {
            'about:author': HTTPStatus.OK,
            'about:tech': HTTPStatus.OK,
        }
        for name, status_code in about_name_urls.items():
            with self.subTest(name=name):
                response = self.guest_client.get(reverse(name))
                self.assertEquals(response.status_code, status_code)

    def test_about_page_uses_correct_template(self):
        """При запросе к 'about:author', 'about:tech'
        применяются верные шаблоны"""
        about_name_urls = {
            'about:author': 'about/author.html',
            'about:tech': 'about/tech.html',
        }
        for name, template in about_name_urls.items():
            with self.subTest(name=name):
                response = self.guest_client.get(reverse(name))
                self.assertTemplateUsed(response, template)
