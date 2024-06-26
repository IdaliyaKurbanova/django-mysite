from django.views.generic import ListView, CreateView
from .models import Article
from django.urls import reverse_lazy


class ArticleListView(ListView):
    queryset = Article.objects.defer('content').select_related('author').select_related('category').prefetch_related(
        'tags')


class ArticleCreateView(CreateView):
    model = Article
    fields = 'title', 'content', 'pub_date', 'author', 'category', 'tags'
    success_url = reverse_lazy('blogapp:article_list')
