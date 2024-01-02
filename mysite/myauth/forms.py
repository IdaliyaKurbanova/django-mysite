from django import forms
from .models import Profile


class OnlyAvatarForm(forms.Form):
    avatar = forms.ImageField(label='To upload new image')

