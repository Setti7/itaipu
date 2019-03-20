from django.db import models

from contas.models import Residente


class Aviso(models.Model):
    data = models.DateTimeField(auto_now_add=True)

    texto = models.TextField()
    autor = models.ForeignKey(Residente, on_delete=models.PROTECT, related_name='avisos')
    titulo = models.CharField(max_length=100, verbose_name='título')
    subtitulo = models.CharField(max_length=200, verbose_name='subtítulo', null=True, blank=True)

    viewers = models.ManyToManyField(Residente, through='AvisoViewer')

    def __str__(self):
        return str(self.titulo)

    class Meta:
        db_table = 'Aviso'


class AvisoViewer(models.Model):
    aviso = models.ForeignKey(Aviso, on_delete=models.CASCADE)
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE, related_name='avisos_visualizados')

    data_visualizado = models.DateTimeField(null=True, blank=True,
                                            help_text='Is set when user sees the warning in details')

    # TODO: maybe add time spent reading just for fun?
    #  Javascript could send a post request every 30 seconds to the server, with the time the page opened. Then the
    #  server just needs to calculate the difference between these times and update the database with the value. If the
    #  user keeps reading for more than 30 seconds, the server would receive another POST with the same "start" time,
    #  which it would use to recalculate the time it took for the user to read.

    class Meta:
        unique_together = ('aviso', 'residente')
        db_table = 'Aviso_viewer'

    def __str__(self):
        return f"{self.aviso.titulo} ({self.residente})"
