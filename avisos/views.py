from django.views.generic import ListView
from .models import Aviso

class AvisoListView(ListView):
    model = Aviso
    paginate_by = 10  # if pagination is desired
    template_name = 'avisos/avisos.html'
    queryset = Aviso.objects.order_by('-data')
    ordering = ['data']