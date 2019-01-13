from uuid import uuid4

from django.core.management.base import BaseCommand
from django.db import connection

from contas.models import Residente
from .tokens_pdf import gen_pdf

def token_generator():
	return uuid4().hex[:8]


class Command(BaseCommand):
	help = 'Gera tokens aleatórios para todos os usários.'

	def handle(self, *args, **options):

		residentes_da_chacara_0 = []

		for n, residente in enumerate(Residente.objects.all().order_by("chacara__id")):
			token = token_generator()

			if residente.chacara is not None:
				if residente.chacara.id == 0:
					residentes_da_chacara_0.append(residente)
					residente.chacara = None

			residente.token = token
			residente.save()

		# self.stdout.write(self.style.SUCCESS('Criado token para "%s" da %s' % (residente.nome, residente.chacara)))

		cursor = connection.cursor()

		# Por algum motivo não pode usar o django para colocar a chacara de residentes como 0.
		for residente in residentes_da_chacara_0:
			cursor.execute(f'''UPDATE Residente SET chac_ID = 0 WHERE nome = "{residente.nome}";''')

		self.stdout.write(self.style.SUCCESS('Criado tokens aleatórios para %s usuários' % n))

		self.stdout.write('Criando PDF com os novos tokens dos residentes.')

		path = gen_pdf()

		self.stdout.write(self.style.SUCCESS(f'PDF criado com sucesso em :{path}'))
