from django.test import TestCase


class CoreViewTests(TestCase):
    def test_core_pages_uses_correct_template(self):
        """URL-адрес в core использует соответствующий шаблон."""
        response = self.client.get('/unexisting_page/')
        self.assertTemplateUsed(response, 'core/404.html')
