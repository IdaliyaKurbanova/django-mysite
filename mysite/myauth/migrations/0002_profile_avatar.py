# Generated by Django 4.2.7 on 2023-12-29 20:41

from django.db import migrations, models
import myauth.models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=myauth.models.get_avatar_file_name),
        ),
    ]