from django.urls import path
from . import views  

app_name = 'news'

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('<int:pk>/', views.article_detail, name='article_detail'),
]
