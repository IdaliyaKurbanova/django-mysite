import datetime

from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    bio = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.name!r}"


class Category(models.Model):
    name = models.CharField(max_length=40, null=False)

    def __str__(self) -> str:
        return f"Category {self.name!r}"


class Tag(models.Model):
    name = models.CharField(max_length=20, null=False)

    def __str__(self) -> str:
        return f"{self.name!r}"


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=False)
    pub_date = models.DateTimeField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='articles')


