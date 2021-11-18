from django.shortcuts import HttpResponse


# Функция обработки главной страницы
def index(request):
    return HttpResponse('Главная страница')


# Функция обработки групп
def group_posts(request, pk):
    return HttpResponse(f'Пост группы {pk}')

# Create your views here.
