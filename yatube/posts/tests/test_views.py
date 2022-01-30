import shutil
import tempfile

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.models import Follow, Group, Post

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.user1 = User.objects.create_user(username='user_test1')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.group2 = Group.objects.create(
            title='Тестовая группа2',
            slug='test-slug2',
            description='Тестовое описание2',
        )
        cls.image = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.image,
            content_type='image/gif',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=PostViewTests.group,
            image=PostViewTests.uploaded,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostViewTests.user)
        self.authorized_client1 = Client()
        self.authorized_client1.force_login(PostViewTests.user1)

    # Проверяем используемые шаблоны
    def test_posts_pages_uses_correct_template(self):
        """URL-адрес в posts использует соответствующий шаблон."""
        templates_page_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list', kwargs={'slug': PostViewTests.group.slug}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile', kwargs={'username': PostViewTests.post.author}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail', kwargs={'post_id': PostViewTests.post.id}
            ): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse(
                'posts:post_edit', kwargs={'post_id': PostViewTests.post.id}
            ): 'posts/create_post.html',
        }
        for reverse_name, template in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # Проверяем, что типы полей формы в словаре context
    # соответствуют ожиданиям
    def test_posts_index_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_author_0 = first_object.author.username
        post_text_0 = first_object.text
        self.assertEqual(post_author_0, PostViewTests.post.author.username)
        self.assertEqual(post_text_0, PostViewTests.post.text)
        self.assertEqual(first_object.image, PostViewTests.post.image)
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_posts_index_add_cash(self):
        """Шаблон index сохраняется в кэш"""
        post = Post.objects.create(
            author=self.user,
            text='Тестовый пост5',
            group=PostViewTests.group,
            image=PostViewTests.uploaded,
        )
        posts_count_before = Post.objects.count()
        response_1 = self.authorized_client.get(reverse('posts:index'))
        post.delete()
        posts_count = Post.objects.count()
        response_2 = self.authorized_client.get(reverse('posts:index'))
        posts_count = Post.objects.count()
        self.assertEqual(posts_count, posts_count_before - 1)
        self.assertEqual(response_1.content, response_2.content)
        cache.clear()
        response_3 = self.authorized_client.get(reverse('posts:index'))
        self.assertNotEqual(response_1.content, response_3.content)

    def test_posts_group_list_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:group_list', kwargs={'slug': PostViewTests.group.slug})
        )
        group_name = response.context['group']
        first_object = response.context['page_obj'][0]
        post_group_0 = first_object.group
        self.assertEquals(group_name, PostViewTests.post.group)
        self.assertEqual(post_group_0, PostViewTests.post.group)
        self.assertEqual(first_object.image, PostViewTests.post.image)
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_posts_group_list_show_correct_context_other_group(self):
        """Шаблон group_list сформирован с правильным контекстом,
        для второй группы."""
        response = self.authorized_client.get(reverse(
            'posts:group_list', kwargs={'slug': PostViewTests.group2.slug})
        )
        self.assertEqual(len(response.context['page_obj']), 0)

    def test_posts_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': PostViewTests.post.author})
        )
        post_count = response.context['posts_count']
        post_author = response.context['author'].username
        self.assertEquals(post_count, 1)
        self.assertEqual(post_author, PostViewTests.post.author.username)
        self.assertEqual(
            response.context['page_obj'][0].image, PostViewTests.post.image
        )
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_posts_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': PostViewTests.post.id})
        )
        self.assertEqual(response.context['post'], PostViewTests.post)
        self.assertEqual(response.context['posts_count'], 1)
        self.assertEqual(
            response.context['post'].image, PostViewTests.post.image)

    def test_posts_post_create_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_posts_post_edit_show_correct_field(self):
        """Шаблон post_edit сформирован с правильными контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': PostViewTests.post.id})
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_posts_post_edit_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом полей."""
        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': PostViewTests.post.id})
        )
        form_fields = {
            PostViewTests.post.text:
            response.context['form']['text'].value(),
            PostViewTests.post.group.id:
            response.context['form']['group'].value(),
        }
        for expected, value in form_fields.items():
            with self.subTest(value=value):
                self.assertEquals(value, expected)

    def test_posts_profile_follow(self):
        """Авторизованный пользователь может подписываться
        на других пользователей"""
        following = Follow.objects.filter(user=self.user1, author=self.user)
        following_count = following.count()
        self.authorized_client1.get(reverse(
            'posts:profile_follow',
            kwargs={'username': PostViewTests.user.username})
        )
        following1 = Follow.objects.filter(user=self.user1, author=self.user)
        following1_count = following1.count()
        self.assertEquals(following_count + 1, following1_count)

    def test_posts_profile_unfollow(self):
        """Авторизованный пользователь может удалять
        других пользователей из подписок"""
        self.authorized_client1.get(reverse(
            'posts:profile_follow',
            kwargs={'username': PostViewTests.user.username})
        )
        following = Follow.objects.filter(user=self.user1, author=self.user)
        following_count = following.count()
        self.authorized_client1.get(reverse(
            'posts:profile_unfollow',
            kwargs={'username': PostViewTests.user.username})
        )
        following1 = Follow.objects.filter(user=self.user1, author=self.user)
        following1_count = following1.count()
        self.assertEquals(following_count, following1_count + 1)

    def test_posts_follow_index(self):
        """Шаблон follow_index сформирован с правильным контекстом полей."""
        user2 = User.objects.create_user(username='test2')
        authorized_client2 = Client()
        authorized_client2.force_login(user2)
        Follow.objects.create(user=self.user1, author=self.user)
        post_user = Post.objects.create(
            author=self.user,
            text='Тестовый пост для user1',
        )
        response1 = self.authorized_client1.get(reverse('posts:follow_index'))
        response2 = authorized_client2.get(reverse('posts:follow_index'))
        last_post_user1 = response1.context['page_obj'][0]
        self.assertEquals(last_post_user1.text, post_user.text)
        self.assertEquals(len(response2.context['page_obj']), 0)


# Проверяем пагинатор
class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        number_posts = 13
        for post_num in range(number_posts):
            Post.objects.create(
                author=cls.user,
                text='Тестовый пост' + str(post_num),
                group=PaginatorViewsTest.group,
            )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PaginatorViewsTest.user)

    def test_paginator_page(self):
        """Количество постов на 1 и 2 страницах index, group_list, profile."""
        templates_page_names = {
            reverse('posts:index'): 10,
            reverse('posts:index') + '?page=2': 3,
            reverse('posts:group_list',
                    kwargs={'slug': PaginatorViewsTest.group.slug}): 10,
            reverse('posts:group_list',
                    kwargs={'slug': PaginatorViewsTest.group.slug})
            + '?page=2': 3,
            reverse('posts:profile',
                    kwargs={'username': PaginatorViewsTest.user}): 10,
            reverse('posts:profile',
                    kwargs={'username': PaginatorViewsTest.user})
            + '?page=2': 3,
        }
        for reverse_name, value in templates_page_names.items():
            with self.subTest(value=value):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), value)
