from django import forms
from .models import Aviso


# https://stackoverflow.com/questions/430592/django-admin-charfield-as-textarea
class AvisoFormAdmin(forms.ModelForm):
    subtitulo = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Aviso
        fields = ['subtitulo']