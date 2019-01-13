from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse

from contas.forms import EditarVisitanteForm, EditarTelefoneForm
from contas.models import Visitante, Movimento


@login_required(redirect_field_name=None)
def editar_visitante(request):
    data = {}
    if request.method == 'POST' and request.is_ajax():
        pk = request.POST.get("form_id")

        try:
            v = Visitante.objects.get(pk=pk)

        except ObjectDoesNotExist:
            data['success'] = False
            data['msg'] = 'Visitante já foi deletado.'
            return JsonResponse(data)

        delete = request.POST.get("delete")
        blacklist = request.POST.get("blacklist")

        # TODO: faça alguma coisa caso user nao seja de nenhuma chacara
        if not request.user.chacara == v.chacara:
            data['success'] = False
            data['msg'] = 'Unauthorized'

        else:

            if delete:
                data['success'] = True
                data['msg'] = '"%s" deletado.' % v.nome

                if Movimento.objects.filter(visitante=v).exists():
                    v.oculto = True
                    v.save()
                else:
                    v.delete()

            elif blacklist:

                v.blacklist = True
                v.nomeres = request.user.nome
                v.save()
                data['success'] = True
                data['msg'] = '"%s" proibido.' % v.nome

            else:

                form = EditarVisitanteForm(request.user.nome, request.POST, instance=v)

                if form.is_valid():
                    data['success'] = True
                    form.save()

                else:
                    data['success'] = False
    else:
        data['success'] = False
        data['msg'] = 'Forbidden'

    return JsonResponse(data)


@login_required(redirect_field_name=None)
def editar_telefone(request):
    data = {}
    if request.method == 'POST' and request.is_ajax():
        c = request.user.chacara

        form = EditarTelefoneForm(request.POST, instance=c)

        if form.is_valid():
            data['success'] = True
            form.save()

        else:
            data['success'] = False
            data['msg'] = form.errors.as_json()

    else:
        data['success'] = False
        data['msg'] = 'Forbidden'

    return JsonResponse(data)
