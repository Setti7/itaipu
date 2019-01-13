from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path, re_path, reverse_lazy

from . import views

app_name = 'contas'
urlpatterns = [
    path('login/', views.CustomLoginView.as_view(template_name='contas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='contas:login'), name='logout'),

    path('associar-conta/', views.associar_conta, name='associar conta'),
    path('associar-conta-email-enviado/', views.associar_conta_email_enviado, name='associar conta email enviado'),
    re_path(r'^ativar-conta/(?P<email_uidb64>[0-9A-Za-z_\-]+)/(?P<token_uidb64>[0-9A-Za-z_\-]+)$',
            views.ativar_conta, name='ativar conta'),

    path('redefinir-senha/', auth_views.PasswordResetView.as_view(
        html_email_template_name='registration/password_reset_email.html',
        from_email=settings.ACCOUNT_RECOVERY_EMAIL,
        success_url=reverse_lazy('contas:password_reset_done')
    ), name='password_reset'),

    path('redefinir-senha/email-enviado/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('redefinir-senha/token/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('contas:password_reset_complete')
    ), name='password_reset_confirm'),

    path('redefinir-senha/pronto/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
