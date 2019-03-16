import json

# Importing envvars from env.json:
def get_envvar(var, alt=None):
    with open('setup/env.json', 'r') as f:
        data = json.loads(f.read())
        return data.get(var, alt)


def gen_SECRET_KEY():
    import random
    SECRET_KEY = ''.join(
        [random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])

    with open('setup/env.json', 'r') as f:
        data = json.loads(f.read())

    with open('setup/env.json', 'w') as f:
        data['SECRET_KEY'] = SECRET_KEY

        f.write(json.dumps(data, indent=4))