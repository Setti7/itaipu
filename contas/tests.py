from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from .forms import AssociarResidenteForm
from .models import Residente


class AssociarResidenteFormTestCase(TestCase):

    def setUp(self):
        self.user = Residente.objects.create_user('test@gmail.com', 'senha1234', token='aaaaaaaa')
        self.user_valid = Residente.objects.create_user('test-valid@gmail.com', 'senha1234', token='bbbbbbbb',
                                                        is_active=True)
        self.factory = RequestFactory()

    def test_associar_residente_form(self):
        """
        Testa se o uma form válida está sendo aceita
        """
        form_data = {
            'email': 'email-unico@gmail.com',
            'new_password1': 'senha1234',
            'new_password2': 'senha1234',
            'token': 'aaaaaaaa'
        }

        request = self.factory.get(reverse('contas:associar conta'))
        request.user = self.user

        form = AssociarResidenteForm(request, data=form_data)
        self.assertTrue(form.is_valid())

        with self.settings(EMAIL_BACKEND='django.core.mail.backends.dummy.EmailBackend'):
            form.save()
            self.assertFalse(self.user.is_active)
            self.assertEqual(form.cleaned_data['email'], 'email-unico@gmail.com')

    def test_associar_residente_form_errors(self):
        """
        Testa se o uma form inválida está processando os erros corretamente
        """
        form_data = {
            'email': 'test@gmail.com',
            'new_password1': 'senha1234',
            'new_password2': 'senha1234',
            'token': '12345678'
        }

        response = self.client.post(reverse('contas:associar conta'), form_data)

        self.assertFormError(response, 'form', 'token', 'Esse token é inválido.')
        self.assertFormError(response, 'form', 'email', 'Esse email já está em uso.')

    def test_associar_conta_em_uso(self):
        """
        Testa se o uma form de uma conta já ativada retorna o erro adequado
        """
        form_data = {
            'email': 'email-nao-usado@gmail.com',
            'new_password1': 'senha1234',
            'new_password2': 'senha1234',
            'token': 'bbbbbbbb'
        }

        response = self.client.post(reverse('contas:associar conta'), form_data)

        self.assertFormError(response, 'form', 'token',
                             'Esse token já foi utilizado.<br>Caso tenha esquecido a senha, vá para a página de '
                             'login e clique em "Esqueceu a senha?".')

    def test_associar_conta_senhas_diferentes(self):
        """
        Testa se o uma form com senhas diferentes retorna o error adequado
        """
        form_data = {
            'email': 'email-nao-usado@gmail.com',
            'new_password1': 'senha12345',
            'new_password2': 'senha1234',
            'token': 'aaaaaaaa'
        }

        response = self.client.post(reverse('contas:associar conta'), form_data)

        self.assertFormError(response, 'form', 'new_password2', 'Os dois campos de senha não combinam.')


class ResidenteForm(TestCase):

    def setUp(self):
        self.user = Residente.objects.create_user('test@gmail.com', 'senha1234', token='aaaaaaaa')

    def test_novo_residente_inativo(self):
        """Testa se novos usaários tem como padrão is_active == False"""
        self.assertFalse(self.user.is_active)
