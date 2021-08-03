from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment
from django.template.backends.jinja2 import Jinja2
from django.utils.timezone import now

# class CustomJinja2(Jinja2):
#     app_dirname = 'templates'


def environment(**options):
    env = Environment(**options, extensions=[])
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        "now": now
    })
    return env
