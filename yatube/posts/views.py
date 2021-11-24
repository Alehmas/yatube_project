from django.shortcuts import HttpResponse, render

from .models import Post, Group


# Функция обработки главной страницы
def index(request):
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)

# Функция обработки групп
def group_posts(request, pk):
    group = get_object_or_404(Group, pk=pk)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)

""" Функция обработки главной страницы
def index(request):
    template = 'posts/index.html'
    title = "Это главная страница проекта Yatube"
    context = {
        'title': title,
    }
    return render(request, template, context)

Функция обработки групп
def group_posts(request, pk):
    template = 'posts/group_list.html'
    title = "Здесь будет информация о группах проекта Yatube"
    context = {
        'title': title,
    }
    print(pk)
    return render(request, template, context)
"""
# Create your views here.
