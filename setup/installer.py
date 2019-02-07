import json

import utils


def main():
    while True:
        ans = utils.question(
            "[ 1 ] Definir ou alterar constantes.\n[ 2 ] Instalar.\n[ 3 ] Sair\n",
            ['1', '2', '3'],
            print_options=False
        )

        if ans == '1':
            result = utils.define_constants()

            print('\n--------------------\nVerfique se os dados abaixo estão corretos:\n')
            for k, v in result.items():
                print(f'{k}: {v}')

            print("--------------------\n")

            result['secret_key'] = utils.create_secret_key()

            with open('env.json', 'w') as f:
                json.dump(result, f, indent=2)

        elif ans == '2':
            print('Instalando...')
            # TODO: perguntar se os dados estão corretos antes da instalação
            # TODO: fazer lista com todos os steps de instalação, perguntando antes se quer executar cada um (pressione enter para proseguir ou qualquer outro otao para pular esse passo)

        elif ans == '3':
            break


if __name__ == '__main__':
    main()
