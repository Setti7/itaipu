import os
from math import ceil

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import FileResponse
from django.shortcuts import render, redirect, Http404

from contas.forms import EditarVisitanteForm, NovoVisitante
from contas.models import Visitante
from django.views import View

@login_required(redirect_field_name=None)
def home(request):
	return render(request, 'core/home.html')


def error(request, code):
	code_list = ['400', '403', '403_csrf', '404', '500']

	if code in code_list:
		return render(request, f'{code}.html')

	else:
		return Http404()


@login_required(redirect_field_name=None)
def configs(request):
	if request.method == 'POST':

		change_password_form = PasswordChangeForm(request.user, request.POST)

		if change_password_form.is_valid():
			change_password_form.save()

			messages.success(request, 'Senha alterada com sucesso!')

			login(request, request.user)
			return redirect('core:home')

		else:
			messages.error(request, 'Houve um erro ao alterar sua senha')

	else:
		change_password_form = PasswordChangeForm(request.user)

	return render(request, 'core/configs.html',
				  {
					  'change_password_form': change_password_form,
				  })


@login_required(redirect_field_name=None)
def autorizar_visitas_blacklist(request, page):
	formset = []

	if page <= 0:
		return redirect("core:autorizar visitas blacklist", page=1)

	# Elements per page
	epp = 36

	cut_start = (page - 1) * epp
	cut_end = (page - 1) * epp + epp

	query = Visitante.objects.filter(chacara=request.user.chacara, oculto=False, blacklist=True).order_by('nome')

	last_page = ceil(len(query) / epp)
	empty = True if last_page == 0 else False

	if page > last_page and not empty:
		return redirect("core:autorizar visitas blacklist", page=last_page)

	if page > 3:
		pages_start = page - 3
		pages_end = page + 2

	else:
		pages_start = 0
		pages_end = 5

	list_of_pages = [i + 1 for i in range(pages_start, pages_end)]

	for c, v in enumerate(query[cut_start:cut_end]):
		form = EditarVisitanteForm(request.user.nome, initial={
			'nome': v.nome,
			'data': v.data,
			'form_id': v.pk,
			'nomeres': v.nomeres
		})
		formset.append(form)

	return render(request, 'core/autorizar_visitas.html',
				  {'formset': formset,
				   'page': page,
				   'previous_page': page - 1 if page > 0 else 0,
				   'next_page': page + 1,
				   'list_of_pages': list_of_pages,
				   'last_page': last_page,
				   'empty': empty,
				   })


@login_required(redirect_field_name=None)
def autorizar_visitas(request, page):
	formset = []

	if page <= 0:
		return redirect("core:autorizar visitas", page=1)

	# Elements per page
	epp = 36

	cut_start = (page - 1) * epp
	cut_end = (page - 1) * epp + epp

	query = Visitante.objects.filter(chacara=request.user.chacara, oculto=False, blacklist=False).order_by('nome')

	last_page = ceil(len(query) / epp)
	empty = True if last_page == 0 else False

	if page > last_page and not empty:
		return redirect("core:autorizar visitas", page=last_page)

	if page > 3:
		pages_start = page - 3
		pages_end = page + 2

	else:
		pages_start = 0
		pages_end = 5

	list_of_pages = [i + 1 for i in range(pages_start, pages_end)]

	for c, v in enumerate(query[cut_start:cut_end]):
		form = EditarVisitanteForm(request.user.nome, initial={
			'nome': v.nome,
			'data': v.data,
			'form_id': v.pk,
			'nomeres': v.nomeres
		})
		formset.append(form)

	return render(request, 'core/autorizar_visitas.html',
				  {'formset': formset,
				   'page': page,
				   'previous_page': page - 1 if page > 0 else 0,
				   'next_page': page + 1,
				   'list_of_pages': list_of_pages,
				   'last_page': last_page,
				   'empty': empty,
				   })


@login_required(redirect_field_name=None)
def novo_visitante(request):
	if request.method == 'POST':

		form = NovoVisitante(request.user, request.POST)

		if form.is_valid():
			form.save()
			messages.success(request, 'Visitante adicionado com sucesso!')

			return redirect('core:novo visitante')

	else:
		form = NovoVisitante(request.user)

	return render(request, 'core/novo_visitante.html', {'form': form})


@staff_member_required(redirect_field_name=None)
def token_pdf(request):
	try:
		return FileResponse(open(os.path.join(settings.BASE_DIR, 'tokens.pdf'), 'rb'), content_type='application/pdf')
	except FileNotFoundError:
		raise Http404()


class EditarChacara(View):

	def get(self, request):
		return render(request, 'core/editar-chacara.html')