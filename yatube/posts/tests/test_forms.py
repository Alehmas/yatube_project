import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..forms import PostForm
from ..models import Group, Post

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostsCreateFormTests.user)

    def test_create_posts_in_base(self):
        """Создаётся новая запись в базе данных,
        cо страницы создания поста create_post."""
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Тестовый пост2',
            'group': self.group.id,
            'image': uploaded,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        new_post = Post.objects.order_by('id').last()
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': PostsCreateFormTests.user}))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(new_post.text, form_data['text'])
        self.assertEqual(new_post.group.id, form_data['group'])
        self.assertEqual(
            new_post.image.name, ('posts/' + form_data['image'].name)
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

    def test_posts_comments(self):
        """Создается комментарий"""
        post = Post.objects.last()
        comments_count = post.comments.count()
        form_data = {
            'text': 'Тестовый комментарий',
        }
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': post.id}),
            data=form_data,
            follow=True
        )
        comment = post.comments.last()
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': post.id}))
        self.assertEqual(post.comments.count(), comments_count + 1)
        self.assertEqual(comment.text, form_data['text'])
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post_id, post.id)

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
