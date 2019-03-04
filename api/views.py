from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from contas.forms import EditarTelefoneForm
from contas.forms import EditarVisitanteForm, EditarResidenteForm
from contas.models import Movimento
from contas.models import Visitante, Residente, Chacara
from api.exceptions import NotAuthorized
from django.http import QueryDict

@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class EditarTelefone(View):

    def post(self, request):
        data = {}
        c = request.user.chacara
        print(request.POST)

        form = EditarTelefoneForm(request.POST, instance=c)

        if form.is_valid():
            data['success'] = True
            form.save()
            print('CHANGED')

        else:
            data['success'] = False
            data['msg'] = form.errors.as_json()
            print('NOT CHANGED')

        return JsonResponse(data)


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class EditarMorador(View):

    def _auth(self, request):
        data = {}

        try:
            r, r_chac = self._get_db_models(request)

        # Handling error if residente does not exist
        except ObjectDoesNotExist:
            data['success'] = False
            raise NotAuthorized(data)

        # Handling error if user is not bounded to a chacara
        except Chacara.DoesNotExist:
            data['success'] = False
            data['msg'] = 'Residente não está registrado à uma chácara.'
            raise NotAuthorized(data)

        if not request.user.chacara == r_chac:
            data['success'] = False
            data['msg'] = 'Não autorizado.'
            raise NotAuthorized(data)

        return r

    def _get_db_models(self, request):
        data = QueryDict(request.body)

        residente = Residente.objects.get(pk=data.get("form_id"))
        residente_chac = request.user.chacara

        return residente, residente_chac

    def post(self, request):
        data = {}

        try:
            r = self._auth(request)

        except NotAuthorized as e:
            return JsonResponse(e.data)

        post_request = request.POST.copy()
        post_request['status'] = r.status
        post_request['token'] = r.token

        form = EditarResidenteForm(post_request, instance=r)

        if form.is_valid():
            data['success'] = True
            form.save()

        else:
            data['success'] = False

        return JsonResponse(data)

    def delete(self, request):
        data = {}

        try:
            r = self._auth(request)

        except NotAuthorized as e:
            return JsonResponse(e.data)

        # TODO: check for user to not delete itself (change ui for button to be disabled)

        if request.user == r:
            return JsonResponse({'success': False, 'msg': 'Você não pode deletar a si mesmo.'})

        data['success'] = True
        data['msg'] = '"%s" deletado.' % r.nome
        r.delete()

        return JsonResponse(data)


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class EditarVisitante(View):

    def _auth(self, request):
        data = {}

        # Handling error if visitante does not exist
        try:
            v, v_chac = self._get_db_models(request)

        except ObjectDoesNotExist:
            data['success'] = False
            data['msg'] = 'Visitante já foi deletado.'
            raise NotAuthorized(data)

        # handling error if visitante is not bounded to a chacara
        except Chacara.DoesNotExist:
            data['success'] = True
            data['msg'] = 'Visitante não estava relacionado com uma chácara, mas foi deletado.'
            v.delete()
            raise NotAuthorized(data)

        # Handling error if user is not bounded to a chacara
        try:
            r_chac = request.user.chacara

        except Chacara.DoesNotExist:
            data['success'] = False
            data['msg'] = 'Residente não está registrado à uma chácara.'
            raise NotAuthorized(data)

        if not r_chac == v_chac:
            data['success'] = False
            data['msg'] = 'Não autorizado.'
            raise NotAuthorized(data)

        return v

    def _get_db_models(self, request):
        data = QueryDict(request.body)

        v = Visitante.objects.get(pk=data.get('form_id'))
        v_chac = v.chacara

        return v, v_chac

    def post(self, request):
        data = {}
        blacklist = request.POST.get("blacklist")

        try:
            v = self._auth(request)

        except NotAuthorized as e:
            return JsonResponse(e.data)

        if blacklist:

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

        return JsonResponse(data)

    def delete(self, request):
        data = {}

        try:
            v = self._auth(request)

        except NotAuthorized as e:
            return JsonResponse(e.data)

        data['success'] = True
        data['msg'] = '"%s" deletado.' % v.nome

        if Movimento.objects.filter(visitante=v).exists():
            v.oculto = True
            v.save()

        else:
            v.delete()

        return JsonResponse(data)