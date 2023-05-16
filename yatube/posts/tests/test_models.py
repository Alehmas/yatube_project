from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Test group',
            slug='Test slug',
            description='Test description',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Test post',
        )

    def test_models_have_correct_object_names(self):
        """Check that models have __str__ working correctly."""
        group = PostModelTest.group
        post = PostModelTest.post
        field_str = {
            group: group.title,
            post: (post.text)[:15],
        }
        for model, expected_value in field_str.items():
            with self.subTest(model=model):
                self.assertEqual(expected_value, str(model))

    def test_post_verbose_name(self):
        """Let's check that the Post verbose_name of the model matches the expected one."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Post text',
            'pub_date': 'Date of publication',
            'author': 'Author',
            'group': 'Group',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertAlmostEquals(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_post_help_text(self):
        """Let's check that the Post help_text model is the same as expected."""
        post = PostModelTest.post
        field_help_text = {
            'text': 'The text of the new post',
            'group': 'The group to which the post will belong',
        }
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertAlmostEquals(
                    post._meta.get_field(field).help_text, expected_value)
