# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    login as auth_login,
)
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from contas.forms import AssociarResidenteForm
from contas.models import Residente


class CustomLoginView(LoginView):

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())

        # If user does NOT check remember-me box, set session expiry to 0
        if not self.request.POST.get('remember_me', None):
            self.request.session.set_expiry(0)

        return HttpResponseRedirect(self.get_success_url())


def associar_conta_email_enviado(request):
    return render(request, 'contas/associar-conta-email-enviado.html')


def associar_conta(request):
    if request.method == 'POST':

        form = AssociarResidenteForm(request, request.POST)

        if form.is_valid():
            form.save()

            return redirect('contas:associar conta email enviado')

    else:
        form = AssociarResidenteForm(request)

    return render(request, 'contas/associar-conta.html', {'form': form})


def ativar_conta(request, email_uidb64, token_uidb64):
    try:
        email = force_text(urlsafe_base64_decode(email_uidb64))
        token = force_text(urlsafe_base64_decode(token_uidb64))

        user = Residente.objects.get(email=email, token=token)
        user.is_active = True
        user.save()

        validlink = True

    except (TypeError, ValueError, OverflowError, Residente.DoesNotExist):
        validlink = False

    return render(request, 'contas/associar-conta-confirmar.html', {'validlink': validlink})
