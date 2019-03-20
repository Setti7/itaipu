from django.conf import settings


def skip_static_requests(record):
    return_code = int(record.args[1])

    if return_code is not 200:
        return True

    if record.args[0].startswith(f'GET {settings.STATIC_URL}'):
        return False
    return True


def skip_media_requests(record):
    return_code = int(record.args[1])

    if return_code is not 200:
        return True

    if record.args[0].startswith(f'GET {settings.MEDIA_URL}'):
        return False

    return True
