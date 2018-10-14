from django.apps import AppConfig


class ApiAppConfig(AppConfig):
    name = "app.api"
    label = "app.api"

    def ready(self):
        pass
