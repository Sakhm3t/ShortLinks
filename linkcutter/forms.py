from django import forms
from .models import *


class LinksForm(forms.ModelForm):
    class Meta:
        model = Links
        fields = ['full_link', 'short_link']
