# Itaipu


Itaipu é um website para moradores do condomínio poderem gerenciar quem pode visitá-los,
com data marcada.


## Serviço de email:
Por padrão é usado o serviço da [SendGrid](https://sendgrid.com/) para enviar email,
pois eles oferecem até 100 envios diários grátis, mas é possível alterar as
configurações do servidor em `itaipu/itaipu/settings.py` para usar outro serviço
qualquer de SMTP.


## Configurando o servidor automáticamente (ubuntu 18.04):
Para essa função existe o script `itaipu/setup/server-setup.sh`. Que instala, configura
e inicializa o servidor Nginx e django automáticamente, além de permitir gerar um
certificado SSL.

Uso: `source server-setup.sh [--ssl]` (como root)

**Faça um backup da database antes de executar esse script!**

OBS: Só use a opção `--ssl` caso o server já esteja funcionando.


## Terminando a configuração automática:
Quando o script de instalação terminar você ainda precisa seguir esses passos:

1. Editar o arquivo `/var/www/html/itaipu/setup/env.json` e colocar nele as variáveis de ambiente. 
(veja tabela abaixo)

2. Editar `/etc/nginx/sites-enabled/itaipu` e mudar a variável `${DOMAIN}` para o domínio do seu site. 
Exemplo da linha: `server_name www.itaipu.com itaipu.com`

3. Alterar os ícones padrões do site (veja as intruções abaixo).

4. Gerar certificado SSL (veja as intruções abaixo).


## Arquivo de configuração (`setup/env.json`):
Após a configuração automática será pedido que se edite esse arquivo, que
possui todas as variáveis para que o website funcione corretamente.

Local: `/var/www/html/itaipu/setup/env.json`

Neste arquivo é preciso que se especifique as seguintes chaves:


| Chave | Descrição |
| ------ | ------ |
| `SECRET_KEY` | A chave secreta do django, para encriptar emails e cookies, com comprimento de 50 caractéres. |
| `DEBUG` | Deixe como `true` para exibir erros do servidor para todos os usuários (admins sempre veem os erros, mesmo quando essa opção for `false`). |
| `ALLOWED_HOSTS` | Uma lista com os hosts permitidos a executar o website, incluindo o ip estático do servidor e os domínios. |
| `DOMAIN` | O domínio que será usado nos emails. Caso estiver usando SendGrid, é preciso fazer as etapas de verificação de domínio deles. |
| `db_name`| O nome da database do Itaipu. Deixe como: `itaipu` |
| `db_user` | O usuário que acessará a database pelo site. Deixe como `itaipu-web` |
| `db_password` | A senha do usuário (`itaipu-web`) que acessará a database. Caso essa opçao for alterada (o que é recomendado), você tem que mudar manualmente a senha do usuário mysql. |
| `SENDGRID_API_KEY` | A chave API do SendGrid. |

Exemplo:

    {
        "SECRET_KEY": "dzz7^!xz@$ly(*%y#e)&%-sf*^-i6245@)33mr_cn@6i0ynl8i",
        "DEBUG": false,
        "ALLOWED_HOSTS": ["seudominio.com", "www.seudominio.com", "129.14.125.753"],
        "DOMAIN": "seudominio.com",
        "db_name": "itaipu",
        "db_user": "itaipu-web",
        "db_password": "escolha uma senha",
        "SENDGRID_API_KEY": "SG.******************************************************************"
    }


## Gerando um certificado SSL:
1. Execute: `source server-setup.sh --ssl` para instalar os pacotes necessários.

2. Execute: `certbot --nginx --staging -d seudominio.com -d www.seudominio.com`
(escolha a opção de redirecionar tráfego HTTP para HTTPS) e recarregue o nginx
com `systemctl reload nginx`.

3. Agora, ao acessar seu site, deve aparecer uma mensagem de certificado inválido ou algo do
tipo: isso siginifca que o teste funcionou.

4. Execute então `certbot --nginx -d seudominio.com -d www.seudominio.com`, escolhendo
para redirecionar tráfego HTTP para HTTPS e para substituir o certificado já instalado
e recarregue o nginx novamente. Seu site deve estar com um certificado SSL válido.

5. Edite `/var/www/html/itaipu/itaipu/settings.py` e descomente as últimas linhas do
arquivo.

6. Reboot


## Ver PDF com todos os tokens de usuários:
Após a instalação do servidor, vá para http://seu-dominio.com/admin/ e faça login com as
credenciais que você escolheu no processo de instalação. Nessa tela, no topo superior
direito tem o link "ver token dos residentes" que permite baixar um pdf com todos os
tokens dos residentes.

Caso queira gerar uma nova lista de tokens use o comando:

`source venv/bin/activate; python manage.py generatetokens`


## Mudar ícones e imagens:
Todos os ícones e imagens estão são salvos na pasta `/var/www/html/itaipu/static/favicon`.

Para gerar os ícones use o site https://realfavicongenerator.net (usando uma imagem do 
logo do condomínio) e substitua os arquivos desta pasta pelos gerados pelo site.

Para gerar os ícones do facebook e etc use o site https://realfavicongenerator.net/social/
e substitua os arquivos desta pasta pelos gerados pelo site.

Caso queira deixar o website sem ícones, apenas renomeie a pasta para outro nome (ou delete).
