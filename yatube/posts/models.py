from django.contrib.auth import get_user_model
from django.db import models
from pytils.translit import slugify

User = get_user_model()


class Group(models.Model):
    """Model class for creating, deleting and editing a group."""

    title = models.CharField(
        verbose_name='Group',
        max_length=200,
        help_text='The group to which the post will belong'
    )
    slug = models.SlugField(
        verbose_name='Address for the group page',
        max_length=100,
        unique=True,
        help_text=(
            'Specify a unique address for the group page. '
            'Use only Latin characters, numbers, hyphens, and underscores'
        )
    )
    description = models.TextField(verbose_name='Description')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Post(models.Model):
    """Model class for creating, deleting and editing a post."""

    text = models.TextField(
        verbose_name='Post text',
        max_length=200,
        help_text='The text of the new post'
    )
    pub_date = models.DateTimeField(
        verbose_name='Date of publication',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        verbose_name='Group',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        help_text='The group to which the post will belong'
    )
    image = models.ImageField(
        'Picture',
        upload_to='posts/',
        blank=True
    )

    def __str__(self):
        return (self.text)[:15]

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comment(models.Model):
    """Model class for creating, deleting and editing a comment."""

    post = models.ForeignKey(
        Post,
        verbose_name='Commentary',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Comment text',
        max_length=200,
        help_text='Text of the new commentary'
    )
    created = models.DateTimeField(
        verbose_name='Date of publication',
        auto_now_add=True
    )

    def __str__(self):
        return (self.text)[:15]


class Follow(models.Model):
    """Model class for creating and deleting a subscription."""

    user = models.ForeignKey(
        User,
        verbose_name='Follower',
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_following')
        ]
