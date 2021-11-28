from django.shortcuts import HttpResponse, render

from .models import Post


# Функция обработки главной страницы
def index(request):
    template = 'posts/index.html'
    title = "Это главная страница проекта Yatube"
    context = {
        'title': title,
    }
    return render(request, template, context)

# Функция обработки групп
def group_posts(request, pk):
    template = 'posts/group_list.html'
    title = "Здесь будет информация о группах проекта Yatube"
    context = {
        'title': title,
    }
    print(pk)
    return render(request, template, context)


# Create your views here.
