from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User


def index(request):
    """Home page processing function"""
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/index.html'
    title = 'Recent updates to the site'
    context = {
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, template, context)


def group_posts(request, slug):
    """Group page processing function"""
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/group_list.html'
    title = f'Community posts {group}'
    context = {
        'group': group,
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, template, context)


def profile(request, username):
    """User page processing function"""
    author = get_object_or_404(User, username=username)
    template = 'posts/profile.html'
    title = f'User profile {author.get_full_name()}'
    post_list = author.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts_count = paginator.count
    user = request.user
    follow_status = (
        user.is_authenticated
        and Follow.objects.filter(user=user, author=author).exists()
    )
    context = {
        'page_obj': page_obj,
        'title': title,
        'posts_count': posts_count,
        'author': author,
        'following': follow_status,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    """Post page processing function"""
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()
    form = CommentForm()
    posts_count = post.author.posts.all().count()
    title = f'Пост {post.text[:30]}'
    context = {
        'post': post,
        'posts_count': posts_count,
        'title': title,
        'form': form,
        'comments': comments,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    """Create a post function"""
    template = 'posts/create_post.html'
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        form.save(commit=False)
        form.instance.author = request.user
        form.save()
        return redirect('posts:profile', request.user)
    return render(request, template, {'form': form})


@login_required
def post_edit(request, post_id):
    """Edit post function"""
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    if form.is_valid():
        post.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'post': post,
        'is_edit': True,
        'form': form,
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    """Comment creation function"""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """Subscriptions display function"""
    posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = "Selected authors' posts"
    context = {
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    """Create a subscription function"""
    author = get_object_or_404(User, username=username)
    user = request.user
    if user != author:
        Follow.objects.get_or_create(user=user, author=author)
    return redirect('posts:profile', author)


@login_required
def profile_unfollow(request, username):
    """Delete subscription function"""
    author = get_object_or_404(User, username=username)
    follow = get_object_or_404(
        Follow, user=request.user, author=author)
    follow.delete()
    return redirect('posts:profile', author)
