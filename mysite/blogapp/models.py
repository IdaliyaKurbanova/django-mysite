from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    bio = models.TextField(blank=True)


class Category(models.Model):
    name = models.CharField(max_length=40, null=False)


class Tag(models.Model):
    name = models.CharField(max_length=20, null=False)


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=False)
    pub_date = models.DateTimeField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='articles')


