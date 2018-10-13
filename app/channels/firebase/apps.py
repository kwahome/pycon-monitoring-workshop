from django.apps import AppConfig


class FirebaseChannelAppConfig(AppConfig):
    name = 'app.channels.firebase'
    label = "app.channels.firebase"

    def ready(self):
        from .routing import FirebaseRoutingHandler
        pass
