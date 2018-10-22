from django.apps import AppConfig


class HTTPBINChannelAppConfig(AppConfig):
    name = 'app.channels.httpbin'
    label = "app.channels.httpbin"

    def ready(self):
        from .routing import HTTPBINRoutingHandler
        pass
