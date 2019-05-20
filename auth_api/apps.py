import sys

from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'auth_api'

    def ready(self):
        import threading

        import auth_api.models
        from auth_api import broker

        # Provee el servicio de generar JWT
        autenticacion_JWT = broker.MessageBrokerServer(queue_name='obtener_jwt', callback=broker.autenticar_usuario)
        threading.Thread(target=autenticacion_JWT.listen).start()

        # Provee el servicio de autenticar a los usuarios con JWT
        validar_JWT = broker.MessageBrokerServer(queue_name='validar_jwt', callback=broker.validar_jwt)
        threading.Thread(target=validar_JWT.listen).start()
