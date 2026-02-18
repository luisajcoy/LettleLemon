from rest_framework import serializers
from django.contrib.auth.models import User

# Serializer para mostrar informacion de usuario
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']
