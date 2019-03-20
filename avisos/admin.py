from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Aviso
from .models import AvisoViewer
from .forms import AvisoFormAdmin


@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    fields = ['titulo', 'subtitulo', 'data', 'texto', 'autor', 'editado_por']
    list_display = ('titulo', 'subtitulo', 'autor', 'data')
    search_fields = ('titulo', 'subtitulo', 'autor', 'texto')

    readonly_fields = ['autor', 'editado_por', 'data']

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

    form = AvisoFormAdmin
    date_hierarchy = 'data'

    def save_model(self, request, obj, form, change):

        if change:
            obj.editado_por = request.user

        else:
            obj.autor = request.user
        obj.save()


@admin.register(AvisoViewer)
class AvisoViewerAdmin(admin.ModelAdmin):

    fields = ['aviso', 'residente', 'data_visualizado']
    list_display = ('aviso', 'residente', 'data_visualizado')
    search_fields = ('aviso', 'residente')

    autocomplete_fields = ['residente', 'aviso']
    date_hierarchy = 'data_visualizado'
