from django.apps import AppConfig


class AfricasTalkingChannelAppConfig(AppConfig):
    name = 'app.channels.at'
    label = "app.channels.at"

    def ready(self):
        from .routing import AfricasTalkingRoutingHandler
        pass
