from django.urls import path
from .views import file_upload

app_name = 'requestdataapp'

urlpatterns = [
    path('file/', file_upload, name='file-upload'),
]
