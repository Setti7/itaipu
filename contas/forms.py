from django import forms
from django.contrib.auth import (
    password_validation,
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.forms import widgets
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from contas.models import Residente, Visitante, Chacara
from itaipu.settings import REGISTRATION_EMAIL


class AssociarResidenteForm(forms.Form):
    token = forms.CharField(max_length=8)
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput,
    )
    email = forms.EmailField(max_length=254)

    field_order = ['token', 'email', 'new_password1', 'new_password2']
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'invalid_token': 'Esse token é inválido.',
        'email_not_unique': "Esse email já está em uso.",
        'account_already_activated': 'Esse token já foi utilizado.<br>Caso tenha esquecido a senha, vá para a página de '
                                     'login e clique em "Esqueceu a senha?".',
    }

    email_template_name = 'contas/associar-residente-email.html'
    subject = 'Parque Itaipu - Ativação da Conta'

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if Residente.objects.filter(email=email).exists():
            raise forms.ValidationError(
                self.error_messages['email_not_unique'],
                code='email_not_unique',
            )
        return email

    def clean(self):
        cleaned_data = super().clean()

        # Token validation
        token = cleaned_data.get('token')
        qs = Residente.objects.filter(token=token)

        if not qs.exists():
            error = forms.ValidationError(
                self.error_messages['invalid_token'],
                code='invalid_token',
            )
            self.add_error('token', error)
            self.user = None

        else:
            self.user = qs[0]

            # Active user validation
            if self.user.is_active:
                error = forms.ValidationError(
                    self.error_messages['account_already_activated'],
                    code='account_already_activated',
                )
                self.add_error('token', error)

        # Password validation
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                error = forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
                self.add_error('new_password2', error)
        password_validation.validate_password(password2, self.user)

        return cleaned_data

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.user.email = self.cleaned_data['email']

        if commit:
            self.user.save()

            current_site = get_current_site(self.request)

            context = {
                'email': self.user.email,
                'domain': current_site.domain,
                'site_name': current_site.name,
                'email_uidb64': urlsafe_base64_encode(force_bytes(self.user.email)).decode(),
                'user': self.user,
                'token_uidb64': urlsafe_base64_encode(force_bytes(self.cleaned_data['token'])).decode(),
                'protocol': 'https' if self.request.is_secure() else 'http',
            }

            body = loader.render_to_string(self.email_template_name, context)

            send_mail(
                subject=self.subject,
                message=None,
                html_message=body,
                from_email=REGISTRATION_EMAIL,
                recipient_list=[self.user.email]
            )

        return self.user


class EditarVisitanteForm(forms.ModelForm):
    # Editáveis
    data = forms.DateField(label='Data', input_formats=['%d/%m/%Y', '%Y-%m-%d'],
                           widget=widgets.DateInput(format='%d/%m/%Y'))

    # Hidden
    form_id = forms.IntegerField(min_value=0, max_value=999999, widget=forms.HiddenInput)
    nomeres = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Visitante
        fields = ['nome', 'data', 'form_id', 'nomeres']

    def __init__(self, nomeres, *args, **kwargs):
        self.nomeres = nomeres
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        v = super().save(commit=False)

        nome = self.cleaned_data.get('nome')
        data = self.cleaned_data.get('data')
        pk = self.cleaned_data.get('form_id')
        nomeres = self.nomeres

        v = Visitante.objects.get(pk=pk)

        if commit:
            v.nome = nome
            v.data = data
            v.agendado = True
            v.nomeres = nomeres

            v.save()

        return v


class NovoVisitante(forms.ModelForm):
    # Editáveis
    data = forms.DateField(label='Data', input_formats=['%d/%m/%Y', '%Y-%m-%d'],
                           widget=widgets.DateInput(format='%d/%m/%Y'))

    class Meta:
        model = Visitante
        fields = ['nome', 'data']

    def __init__(self, user, *args, **kwargs):
        self.chacara = user.chacara
        self.nomeres = user.nome
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        v = super().save(commit=False)

        nome = self.cleaned_data.get('nome')
        data = self.cleaned_data.get('data')
        chacara = self.chacara
        nomeres = self.nomeres

        if commit:
            v = Visitante.objects.create(nome=nome, chacara=chacara, nomeres=nomeres, data=data)
            v.save()

        return v


class EditarTelefoneForm(forms.ModelForm):
    class Meta:
        model = Chacara
        fields = ['telefone']
