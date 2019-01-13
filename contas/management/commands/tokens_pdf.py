import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from weasyprint import HTML, CSS

from contas.models import Residente


def gen_pdf():
	path = os.path.join(settings.BASE_DIR, 'tokens.pdf')

	residentes = [r for r in Residente.objects.all().order_by('nome')]
	rendered = render_to_string('contas/token_pdf.html', {'residentes': residentes})

	html = HTML(string=rendered)

	css = CSS(string='''
			@page {
				size: A4;
				@bottom-right {
					content: counter(page) " / " counter(pages);
				}
			}
			''')

	html.write_pdf(path, stylesheets=[css])

	return path


class Command(BaseCommand):
	help = 'Cria um arquivo PDF com todos os tokens dos usuários.'

	def handle(self, *args, **options):
		self.stdout.write('Criando PDF com os tokens dos residentes.')

		path = gen_pdf()

		self.stdout.write(self.style.SUCCESS(f'PDF criado com sucesso. em {path}'))
