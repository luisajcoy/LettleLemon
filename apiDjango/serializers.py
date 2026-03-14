from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, MenuItem, Orden, OrdenItem, Cart

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
    
# Serializer OrdenItem
class OrdenItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenItem
        fields = ['id', 'menuitem', 'quantity', 'unit_price', 'price']
        
        
# Serializer Orden 
class OrdenSerializer (serializers.ModelSerializer):
    
    # El source es el acceso interno al campo en la tabla orden para acceder a los items de la orden
    items = OrdenItemSerializer(many=True, read_only =True, source='ordenitem_set' )
    class Meta:
        model = Orden
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
        
        
# Serializer status de order
class OrdenStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orden
        fields = ['status']
        
    # Verifica si el valor es booleano
    def validate_status(self, value):
        # Validar que el status sea un boolean
        if not isinstance(value,bool):
            raise serializers.ValidationError("El valor debe ser un valor Boolean (True/False)")
        return value

# Serializer de cart 
class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model= Cart
        fields = ['id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']
        read_only_fields = ['unit_price', 'price']

    def create(self, validated_data):
        menuitem_id = validated_data.get('menuitem_id')
        try:
            menuitem = MenuItem.objects.get(id = menuitem_id)
        except MenuItem.DoesNotExist:
            raise serializers.ValidationError({"menuitem_id": "MenuItem no existe"})
        
        # Calcular precio con cantidad
        quantity = validated_data.get('quantity')
        unit_price = menuitem.price
        price = unit_price * quantity

        # Crear item del carrito
        cart_item = Cart.objects.create(
            user = self.context['request'].user,
            menuitem = menuitem,
            quantity = quantity ,
            unit_price = unit_price ,
            price = price
        )
        return cart_item


class OrdenAssignSerializer(serializers.ModelSerializer):
    delivery_crew_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Orden
        fields = ['delivery_crew_id']

    def validate_delivery_crew_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('El repartidor no existe')

        if not user.groups.filter(name='Delivery Crew').exists():
            raise serializers.ValidationError('El usuario no pertenece al grupo Delivery Crew')

        return value

    def update(self, instance, validated_data):
        delivery_crew_id = validated_data.get('delivery_crew_id')
        instance.delivery_crew = User.objects.get(id=delivery_crew_id)
        instance.save()
        return instance

# Actualizar articulo del dia 
class MenuItemFeaturedSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['featured']

    def validate_featured(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError('featured debe ser True o False')
        return value

