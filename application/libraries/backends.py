from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class MobileBackend(ModelBackend):
    """
    This backed has been introduced for mobile no based user
    authentication, which will be consumed by authenticate
    function.
    """
    def authenticate(self, request, username=None, password=None):
        User = get_user_model()
        try:
            user_object = User.objects.get(mobile=username)
            if user_object.check_password(password):
                return user_object
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class EmailBackend(ModelBackend):
    """
    This backed has been introduced for email based user
    authentication, which will be consumed by authenticate
    function.
    """
    def authenticate(self, request, username=None, password=None):

        User = get_user_model()
        try:
            user_object = User.objects.get(email=username)
            if user_object.check_password(password):
                return user_object
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None