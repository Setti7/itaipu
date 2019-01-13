from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse

from contas.forms import EditarVisitanteForm, EditarTelefoneForm
from contas.models import Visitante, Movimento, Chacara, Residente


@login_required(redirect_field_name=None)
def editar_visitante(request):
    data = {}
    if request.method == 'POST' and request.is_ajax():
        pk = request.POST.get("form_id")

        # Handling error if visitante does not exist
        try:
            v = Visitante.objects.get(pk=pk)
        except ObjectDoesNotExist:
            data['success'] = False
            data['msg'] = 'Visitante já foi deletado.'
            return JsonResponse(data)

        # handling error if visitante is not bounded to a chacara
        try:
            v_chac = v.chacara
        except Visitante.chacara.RelatedObjectDoesNotExist:
            data['success'] = True
            data['msg'] = 'Visitante não estava relacionado com uma chácara, mas foi deletado.'
            v.delete()
            return JsonResponse(data)

        # Handling error if user is not bounded to a chacara
        try:
            r_chac = request.user.chacara
        except Residente.chacara.RelatedObjectDoesNotExist:
            data['success'] = False
            data['msg'] = 'Residente não está registrado à uma chácara.'
            return JsonResponse(data)

        delete = request.POST.get("delete")
        blacklist = request.POST.get("blacklist")

        if not r_chac == v_chac:
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
