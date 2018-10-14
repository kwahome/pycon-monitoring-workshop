from django.apps import AppConfig


class CoreAppConfig(AppConfig):
    name = "app.core"
    label = "app.core"

    def ready(self):
        pass
