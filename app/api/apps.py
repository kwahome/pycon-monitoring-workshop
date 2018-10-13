from django.apps import AppConfig


class ApiAppConfig(AppConfig):
    name = "app.api"
    label = "api"

    def ready(self):
        pass
