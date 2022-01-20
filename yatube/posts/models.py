from django.contrib.auth import get_user_model
from django.db import models
from pytils.translit import slugify

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        verbose_name='Группа',
        max_length=200,
        help_text='Группа, к которой будет относиться пост'
    )
    slug = models.SlugField(
        verbose_name='Адрес для страницы группы',
        max_length=100,
        unique=True,
        help_text=(
            'Укажите уникальный адрес для страницы группы. Используйте только '
            'латиницу, цифры, дефисы и знаки подчёркивания'
        )
    )
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста',
        max_length=200,
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        verbose_name='Группа',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        help_text='Выберите группу'
    )

    def __str__(self):
        return (self.text)[:15]

    class Meta:
        ordering = ['-pub_date']
