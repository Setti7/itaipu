from itaipu.settings import EMAIL_ADMIN_SHOW


def constants_processor(request):
    c = {'EMAIL_ADMIN': EMAIL_ADMIN_SHOW}
    return c
