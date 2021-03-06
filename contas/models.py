from uuid import uuid4
import os

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .managers import ResidenteManager
from .storage import OverwriteStorage, update_filename

storage = OverwriteStorage()


def token_generator():
    return uuid4().hex[:8]


class Chacara(models.Model):
    id = models.AutoField(db_column='chac_ID', primary_key=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    via = models.CharField(max_length=25)
    lote = models.CharField(max_length=10)
    quadra = models.CharField(max_length=6)
    classe = models.CharField(max_length=6)
    operacao = models.IntegerField()

    @property
    def todos_moradores(self):
        residentes = ["%s" % r.nome for r in self.residentes.all()]
        return ", ".join(residentes)

    @property
    def alguns_visitantes(self):
        v = ["%s" % visitante.nome for visitante in self.visitantes.all()]

        if len(v) == 0:
            return "---"

        elif len(v) > 4:
            txt = ", ".join(v[:4])
            return txt + "..."

        return ", ".join(v)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'chácara'
        verbose_name_plural = 'chácaras'
        db_table = 'Chacara'
        ordering = ['id']


class Visitante(models.Model):
    id = models.AutoField(db_column='vis_ID', primary_key=True)
    nome = models.CharField(max_length=50, db_column='nomevis')
    veiculo = models.CharField(max_length=7, null=True, db_column='veic_ID', blank=True)
    chacara = models.ForeignKey(Chacara, on_delete=models.PROTECT, related_name='visitantes',
                                verbose_name='chácara', db_column='chac_ID')
    nomeres = models.CharField(max_length=50, default='DESCONHECIDO', db_column='nomeres')
    oculto = models.BooleanField(default=False, db_column='Oculto')
    blacklist = models.BooleanField(default=False, db_column='Blacklist')
    agendado = models.BooleanField(default=True, db_column='Agendado')
    data = models.DateField(null=True)
    foto = models.ImageField(null=True, blank=True, upload_to=update_filename, storage=storage)

    def __str__(self):
        return str(self.nome)

    class Meta:
        db_table = 'Visitante'


class Movimento(models.Model):
    id = models.AutoField(db_column='mov_ID', primary_key=True)
    visitante = models.ForeignKey(Visitante, verbose_name='visitante', on_delete=models.PROTECT,
                                  db_column='vis_ID')  # vis_ID
    data_entrada = models.DateTimeField()
    data_saida = models.DateTimeField()
    aberto = models.IntegerField()
    aberport_id = models.SmallIntegerField()  # aberport_ID
    fechport_id = models.SmallIntegerField()  # fechport_ID

    def __str__(self):
        return "Movimento de %s" % self.visitante

    class Meta:
        db_table = 'Movimento'


class Residente(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=1, choices=(('C', 'Caseiro'), ('F', 'Funcionário'), ('P', 'Proprietário')),
                              default='P')
    token = models.CharField(max_length=8, unique=True, default=token_generator, null=True)
    chacara = models.ForeignKey(Chacara, related_name='residentes', verbose_name='chácara',
                                on_delete=models.PROTECT, null=True, db_column='chac_id', default=None)  # chac_ID
    email = models.EmailField(null=True, unique=True)

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now, null=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']
    objects = ResidenteManager()

    def __str__(self):
        return str(self.nome)

    def get_full_name(self):
        return str(self.nome)

    def get_short_name(self):
        return str(self.nome)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_absolute_url(self):
        return "%s-%s" % (self.nome, self.pk)

    class Meta:
        unique_together = ["chacara", "nome"]
        db_table = 'Residente'
