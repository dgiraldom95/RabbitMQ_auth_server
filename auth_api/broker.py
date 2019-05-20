#!/usr/bin/env python
import json
import pika
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.serializers import JSONWebTokenSerializer, VerifyJSONWebTokenSerializer
from auth_api.serializers import UserSerializer


class MessageBrokerServer:
    def __init__(self, queue_name, callback):
        # La función que se encarga de procesar el mensaje y manejar la logica
        self.callback = callback
        # El key del canal
        self.routing_key = queue_name
        # Las credenciales del servidor RabbitMQ
        self.credentials = pika.PlainCredentials('atpos', 'atpos')

        # La información de conexión con la dirección del servidor
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='157.230.14.37', port=5672, virtual_host='/', credentials=self.credentials))

        # Inicia el canal
        self.channel = self.connection.channel()

        # Inicia la cola
        self.channel.queue_declare(self.routing_key, exclusive=False)

        # Recibe sobre el canal de respuesta
        self.channel.basic_consume(
            queue=self.routing_key,
            on_message_callback=self.on_request,
            auto_ack=True)

    # Escucha sobre el canal
    def listen(self):
        print('JWT broker listening')
        self.channel.start_consuming()

    def on_request(self, ch, method, props, body):
        data = json.loads(body, encoding='utf-8')

        response = self.callback(data)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=str(response))


def autenticar_usuario(message_json):
    user = message_json['user']
    password = message_json['password']

    serializer_data = {'data': {'cc': user, 'password': password}}
    jwt_serializer = JSONWebTokenSerializer(**serializer_data)
    if jwt_serializer.is_valid():
        user = jwt_serializer.object.get('user')
        token = jwt_serializer.object.get('token')
    else:
        return json.dumps({'error': True})

    respuesta = {'token': token, 'user': UserSerializer(user).data}
    respuesta = json.dumps(respuesta)
    return respuesta


def validar_jwt(message_json):
    token = message_json['token']
    serializer_data = {'data': {'token': token}}

    try:
        validated_data = VerifyJSONWebTokenSerializer().validate({'token': token})

        user = validated_data['user']
        token = validated_data['token']
        respuesta = json.dumps({'user': UserSerializer(user).data, 'token': token})
        return respuesta

    except ValidationError:
        return json.dumps({'error': True})
