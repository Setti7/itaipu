import random


def create_secret_key():
    SECRET_KEY = ''.join(
        [random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for _ in range(50)])

    return SECRET_KEY


def question(text, valid_answers: list, print_options=True):
    ans = f'[ {"/".join(valid_answers)} ]'

    while True:
        if print_options:
            answer = input(f"{text} {ans}")
        else:
            answer = input(f"{text}")

        answer = answer.lower()

        if answer in valid_answers:
            return answer


def define_constants():
    debug = int(input(
        '\nDEBUG\nEm modo debug os erros do website e algumas informações sensíveis são visíveis na própria página.\nÉ essencial que essa constante seja "0" quando o website não estiver mais em fase de testes.\n[ 0/1 ]\n'))
    debug = bool(debug)

    allowed_hosts = input(
        '\nALLOWED_HOSTS\nLista com todos os hosts permitidos de hostearem o website (separados por espaços).\nQuando em modo debug todos os hosts são permitidos. Usar * para aceitar todos os hosts.\n')
    allowed_hosts = allowed_hosts.split(" ")

    db_name = input("\nDATABASE_NAME\nNome da database do website.\nRecomendado: itaipu\n")
    db_user = input(
        "\nDATABASE_USER\nUsuário do mysql e do linux que é usado para controlar o website.\nRecomendado: itaipu-web\n")
    db_password = input(f'\nDATABASE_PASSWORD\nSenha mysql do usuário "{db_user}" previamente definido.\nDICA: Para alterar a senha do usuário mysql use esse comando:\nmysql -u root -p -D {db_name} -e "GRANT ALL PRIVILEGES ON {db_name}.* TO \'{db_user}\'@\'localhost\' IDENTIFIED BY \'sua senha aqui\';\n')

    return {
        'debug': debug,
        'allowed_hosts': allowed_hosts,
        'db_name': db_name,
        'db_user': db_user,
        'db_password': db_password,
    }
