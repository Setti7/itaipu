from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


# https://stackoverflow.com/questions/2680391/how-to-change-the-file-name-of-an-uploaded-file-in-django
def update_filename(instance, filename):
    ext = os.path.splitext(filename)[1]

    name = f"{instance.nome}_{instance.id}{ext}"
    return name


# https://stackoverflow.com/questions/9214904/how-to-prevent-django-from-changing-file-name-when-a-file-with-that-name-already
class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
