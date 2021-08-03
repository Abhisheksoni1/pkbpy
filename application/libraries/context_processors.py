from django.conf import settings
# from apps.user.models import GroupConstants
#from shared.users.models import GroupNameConstants


def load(request):
    context = dict(
        **settings.CUSTOM_DIRS,
        # **{"groups": {key: value for key, value in GroupNameConstants.__dict__.items() if
        #               not key.startswith('__') and not callable(key)}}
    )
    return context


