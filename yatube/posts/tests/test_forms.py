from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Group, Post

User = get_user_model()


class PostsCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostForm()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        Post.objects.create(
            author=cls.user,
            text='Тестовый пост1',
            group=PostsCreateFormTests.group,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostsCreateFormTests.user)

    def test_create_posts_in_base(self):
        """Создаётся новая запись в базе данных,
        cо страницы создания поста create_post."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый пост2',
            'group': PostsCreateFormTests.group.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': PostsCreateFormTests.user}))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.order_by('id').last().text == form_data['text']
        )
        self.assertTrue(
            Post.objects.order_by('id').last().group.id == form_data['group']
        )

    def test_edit_posts_in_base(self):
        """Происходит изменение поста с post_id в базе данных,
        со страницы редактирования поста post_edit"""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый пост3',
            'group': PostsCreateFormTests.group.id
        }
        post = Post.objects.get(id='1')
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': post.id}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': post.id}))
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(
                id='1',
                text='Тестовый пост3'
            ).exists()
        )

    def test_posts_labels(self):
        """У полей формы есть label"""
        form_data = {
            'text': 'Текст поста',
            'group': 'Группа'
        }
        for field, expected in form_data.items():
            self.assertEquals(
                PostsCreateFormTests.form.fields[field].label, expected
            )

    def test_posts_help_text(self):
        """У полей формы есть hepl_text"""
        form_data = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет относиться пост'
        }
        for field, expected in form_data.items():
            self.assertEquals(
                PostsCreateFormTests.form.fields[field].help_text, expected
            )
