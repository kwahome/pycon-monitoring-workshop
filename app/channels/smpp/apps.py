from django.apps import AppConfig


class SMPPChannelAppConfig(AppConfig):
    name = 'app.channels.smpp'
    label = "app.channels.smpp"

    def ready(self):
        from .routing import SMPPRoutingHandler
        pass
