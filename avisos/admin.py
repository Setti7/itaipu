from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Aviso
from .models import AvisoViewer
from .forms import AvisoForm
admin.site.register(AvisoViewer)


@admin.register(Aviso)
class VisitanteAdmin(admin.ModelAdmin):
    fields = ['titulo', 'subtitulo', 'autor', 'texto']
    list_display = ('titulo', 'subtitulo', 'autor', 'data')
    search_fields = ('titulo', 'subtitulo', 'autor', 'texto')

    autocomplete_fields = ['autor']

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

    form = AvisoForm