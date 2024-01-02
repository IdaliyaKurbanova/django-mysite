from django.contrib.auth.models import User
from django.db import models


def get_avatar_file_name(instance: 'Profile', filename) -> str:
    return "profiles/profile_{pk}/{filename}".format(pk=instance.user.pk, filename=filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    agreement_signed = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=get_avatar_file_name)

