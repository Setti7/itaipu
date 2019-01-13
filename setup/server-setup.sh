#!/usr/bin/env bash

#TODO: o que fazer com residentes que estão registrados em 2 chácaras? Minha ideia é unir a lista de
# visitas das duas chácaras na página de autorizar visitas, além de clocar mais um campo para editar
# os telefones das chacarás.


# Settings constants
r='\033[0;31m'
g='\033[0;32m'
b='\033[0;34m'
n='\033[0m' # No Color

# Checando se o script está sendo rodado dentro da pasta setup/
if [ "$(basename "$(pwd)")" != "setup" ]; then
    printf "${r}Rode o script dentro da pasta setup/\n${n}"
    exit 0
fi

CWD="$(pwd)"

function check () {
    # Argumento 1 é o resultado do ultimo comando executado ($?)

    if [ $1 -eq 0 ]; then
        printf "${g}Feito!\n${n}"
    else
        printf "${r}ERRO!\n${n}"
        read -p "Aperte enter para continuar assim mesmo ou ctrl + c para sair." CONTINUE
    fi
}

if [[ $* == *--ssl* ]]; then

    echo -e "${b}Adicionando repositório do certbot${n}"
    add-apt-repository ppa:certbot/certbot -y
    apt-get install python-certbot-nginx software-properties-common
    check $?

    echo -e "${b}Use o comando: \"certbot --nginx [--staging] -d seudominio.com -d www.seudominio.com\"${n}"

    exit 0
fi

# instalando dependências
echo -e "${b}Instalando dependências${n}"
apt-get update
apt-get install python3-pip python3-dev libpq-dev mysql-server nginx curl ufw libmysqlclient-dev default-libmysqlclient-dev python3.6 libpango1.0-0 libcairo2 libpq-dev
check $?


# criando usuario para gerenciar o site
echo -e "${b}Criando usuário gerenciador do site${n}"
useradd 'itaipu-web'
check $?


# Configurando usuário
echo -e "${b}Configurando usuário gerenciador do site (insira a senha root do mysql)${n}"
mysql -u root -p -D itaipu -e "GRANT ALL PRIVILEGES ON itaipu.* TO 'itaipu-web'@'localhost' IDENTIFIED BY 'escolha uma senha';"
check $?


# instalando virtualenv
echo -e "${b}Instalando virtualenv${n}"
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
check $?


# criando projeto
echo -e "${b}Clonando projeto${n}"
git clone https://github.com/Setti7/itaipu.git /var/www/html/itaipu/
check $?


# inicializando virtualenv
echo -e "${b}Inicializando virtualenv${n}"
virtualenv /var/www/html/itaipu/venv
cd /var/www/html/itaipu
source venv/bin/activate
check $?


# instalando reuirements.txt
echo -e "${b}Instalando requirements.txt${n}"
pip install -r requirements.txt
check $?


echo -e "${b}Migrando alterações da database (insira a senha root do mysql)${n}"
cd "${CWD}"
mysql -u root -p itaipu < db_migration.sql
check $?

echo -e "${b}Configurando constantes do website${n}"
cp example_env.json /var/www/html/itaipu/setup/env.json
cd /var/www/html/itaipu
python manage.py migrate --fake
python manage.py collectstatic


echo -e "${b}Criando super-usuário do site${n}"
python manage.py createsuperuser
python manage.py generatetokens
check $?


# configurando gunicorn
echo -e "${b}Configurando gunicorn${n}"
sudo chown -R itaipu-web:www-data /var/www/html/itaipu/
cd "${CWD}"
cp gunicorn.socket /etc/systemd/system/gunicorn.socket
cp gunicorn.service /etc/systemd/system/gunicorn.service
check $?

echo -e "${b}Reiniciando gunicorn${n}"
systemctl start gunicorn.socket
systemctl enable gunicorn.socket
check $?


# configurando nginx
echo -e "${b}Configurando Nginx${n}"
cp itaipu /etc/nginx/sites-available/itaipu
cp itaipu /etc/nginx/sites-enabled/itaipu
cp fastcgi_params /etc/nginx/fastcgi_params
systemctl enable nginx
systemctl restart nginx
check $?


# configurando firewall
echo -e "${b}Configurando firewall do Nginx${n}"
ufw allow 'Nginx Full'
check $?


echo -e "${g}Tudo Pronto!${n}"
echo -e "${g}Leia a parte \"Terminando a configuração automática\" do README para finalizar.${n}"
