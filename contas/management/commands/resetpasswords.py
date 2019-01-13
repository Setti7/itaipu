from django.core.management.base import BaseCommand

from contas.models import Residente


class Command(BaseCommand):
    help = 'Cria senhas inusáveis para todos os residentes.'

    def handle(self, *args, **options):

        n = 0
        for residente in Residente.objects.all():
            residente.set_unusable_password()
            residente.save()
            n += 1

        self.stdout.write(self.style.SUCCESS('Criado senha inusável para %s usuários.' % n))