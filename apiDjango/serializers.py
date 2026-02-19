from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category

# Serializer para mostrar informacion de usuario
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']
        
# Serializer Categoria
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title','slug']
