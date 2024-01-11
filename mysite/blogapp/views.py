from django.shortcuts import render
from django.views.generic import ListView
from .models import Article
import datetime


class ArticleListView(ListView):
    queryset = (
        Article.objects.defer('content').select_related('author').
        select_related('category').prefetch_related('tags'))

