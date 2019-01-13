from contas.forms import EditarTelefoneForm
from itaipu.settings import EMAIL_ADMIN_SHOW


def constants_processor(request):
    c = {'EMAIL_ADMIN': EMAIL_ADMIN_SHOW}

    if request.user.is_authenticated and request.user.chacara is not None:
        form = EditarTelefoneForm(initial={'telefone': request.user.chacara.telefone})
        c['telefone_form'] = form
    return c
