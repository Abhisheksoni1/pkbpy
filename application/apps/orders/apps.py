from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = 'apps.orders'

    def ready(self):
        import api.v1.signals.user_profile
