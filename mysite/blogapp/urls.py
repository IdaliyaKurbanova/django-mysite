from django.urls import path
from .views import ArticleListView, ArticleCreateView

app_name = 'blogapp'

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
]
