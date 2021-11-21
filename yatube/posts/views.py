from django.shortcuts import HttpResponse, render


# Функция обработки главной страницы
def index(request):
    template = 'posts/index.html'
    return render(request, template)


# Функция обработки групп
def group_posts(request, pk):
    return HttpResponse(f'Пост группы {pk}')

# Create your views here.
