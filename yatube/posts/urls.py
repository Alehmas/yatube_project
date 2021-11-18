from django.urls import path

from . import views

urlpatterns = [
    path('posts/', views.index),
    path('posts/<slug:pk>/', views.group_posts),
]
