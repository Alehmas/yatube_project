from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Group, Post, User


def index(request):
    """Функция обработки главной страницы"""
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/index.html'
    title = 'Последние обновления на сайте'
    context = {
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, template, context)


def group_posts(request, slug):
    """Функция обработки главной страницы"""
    group = get_object_or_404(Group, slug=slug)
    template = 'posts/group_list.html'
    title = f'Записи сообщества {group}'
    posts = group.posts.all()[:10]
    context = {
        'group': group,
        'posts': posts,
        'title': title,
    }
    return render(request, template, context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    template = 'posts/profile.html'
    title = f'Профайл пользователя {user.get_full_name()}'
    post_list = Post.objects.filter(author=user).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts_count = paginator.count
    context = {
        'page_obj': page_obj,
        'title': title,
        'posts_count': posts_count,
        'user': user,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    posts_count = Post.objects.filter(author=author).count()
    title = f'Пост {post.text[:30]}'
    context = {
        'post': post,
        'posts_count': posts_count,
        'title': title
    }
    return render(request, template, context)
