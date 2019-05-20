from rest_framework import serializers
from auth_api.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('last_login', )

    def create(self, validated_data):
        cc = validated_data.pop('cc')
        password = validated_data.pop('password')
        nombre = validated_data.pop('nombre')
        email = validated_data.pop('email')

        user = User.objects.create_user(cc, password, email, nombre, **validated_data)
        return user