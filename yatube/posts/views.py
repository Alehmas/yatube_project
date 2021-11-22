from django.shortcuts import HttpResponse, render


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

""" Функция обработки групп
была так оформлена функция до раздела HTML страницы в Django. Render
def group_posts(request, pk):
    return HttpResponse(f'Пост группы {pk}')
"""
# Create your views here.
