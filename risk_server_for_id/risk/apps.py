from django.apps import AppConfig


class RiskConfig(AppConfig):
    name = 'risk'
    def ready(self):
        from . import views
