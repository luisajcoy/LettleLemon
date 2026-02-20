from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, MenuItem

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
        
# Serializer MenuItem
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only = True)
    category_id = serializers.IntegerField(write_only = True)
    
    class Meta:
        model = MenuItem
        fields = ['id','title', 'price', 'featured','category', 'category_id']
    
    def create(self, validated_data):
        # Extraer category_id de los datos validados
        category_id = validated_data.pop('category_id')
        
        # Obtener el objeto Category
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError({"category_id": "Categoría no existe"})
        
        # Crear el MenuItem con el objeto category
        menu_item = MenuItem.objects.create(
            category=category,
            **validated_data
        )
        return menu_item
        
    
