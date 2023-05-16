from django.test import TestCase


class CoreViewTests(TestCase):
    def test_core_pages_uses_correct_template(self):
        """The URL in core uses the appropriate template."""
        response = self.client.get('/unexisting_page/')
        self.assertTemplateUsed(response, 'core/404.html')
